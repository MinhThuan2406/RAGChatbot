import os
import logging
from typing import Dict, Any, List
from pathlib import Path
from pdfminer.high_level import extract_text as extract_pdf_text
import docx
import pytesseract
from PIL import Image
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..db.chroma_client import ChromaDBClient
from ..adapters.openai_adapter import OpenAIAdapter
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading        

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles extraction of text from various document types"""
    @staticmethod
    def get_document_type(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()
        if extension == '.pdf':
            return 'pdf'
        elif extension == '.docx':
            return 'docx'
        elif extension == '.doc':
            return 'doc'
        elif extension == '.txt':
            return 'txt'
        elif extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
            return 'image'
        else:
            raise ValueError(f"Unsupported file type: {extension}")

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        try:
            text = extract_pdf_text(file_path)
            return text or ""
        except Exception as e:
            logger.error(f"Failed to extract text from PDF {file_path}: {e}")
            return ""

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            logger.error(f"Failed to extract text from DOCX {file_path}: {e}")
            return ""

    @staticmethod
    def extract_text_from_doc(file_path: str) -> str:
        logger.error("DOC file support not implemented. Please convert to DOCX.")
        return ""

    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to extract text from TXT {file_path}: {e}")
            return ""

    @staticmethod
    def extract_text_from_image(file_path: str) -> str:
        try:
            image = Image.open(file_path)
            return pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"Failed to extract text from image {file_path}: {e}")
            return ""

    def extract_text(self, file_path: str) -> str:
        doc_type = self.get_document_type(file_path)
        if doc_type == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif doc_type == 'docx':
            return self.extract_text_from_docx(file_path)
        elif doc_type == 'doc':
            return self.extract_text_from_doc(file_path)
        elif doc_type == 'txt':
            return self.extract_text_from_txt(file_path)
        elif doc_type == 'image':
            return self.extract_text_from_image(file_path)
        else:
            return ""

from typing import List
import asyncio

class AsyncEmbeddingFunction:
    """
    Wrapper for async embedding client compatible with ChromaDB.
    Pass an embedding client object (e.g., OpenAIAdapter) that implements async create_embedding(text: str) -> list[float].
    """
    def __init__(self, client, name: str = "openai"):
        self._client = client
        self._name = name

    def __call__(self, texts: list[str]) -> list[list[float]]:
        async def get_embeddings():
            if hasattr(self._client, "embed_documents"):
                return await self._client.embed_documents(texts)
            else:
                return [await self._client.create_embedding(t) for t in texts]
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if loop.is_running():
            return asyncio.run(get_embeddings())
        else:
            return loop.run_until_complete(get_embeddings())

    def name(self):
        return self._name

class IngestionService:
    """
    Service for ingesting documents into the vector database.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, provider: str = ""):
        from .llm_provider_factory import LLMFactory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
        
        # Force OpenAI for embeddings if Ollama is specified
        if self.provider == "ollama":
            logger.warning("Ollama doesn't support embeddings. Switching to OpenAI for embeddings.")
            embedding_provider = "openai"
        else:
            embedding_provider = self.provider
            
        self.embedding_client = LLMFactory.get_embedding_client(embedding_provider)
        
        # Create thread-safe embedding function
        self.embedding_function = AsyncEmbeddingFunction(self.embedding_client, embedding_provider)
        
        self.vector_db_client = ChromaDBClient(embedding_function=self.embedding_function)
        self.document_processor = DocumentProcessor()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        logger.info(f"Initialized IngestionService with {embedding_provider} embeddings.")

    def _is_supported_file(self, file_path: str) -> bool:
        try:
            self.document_processor.get_document_type(file_path)
            return True
        except Exception:
            return False

    async def ingest_document(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """Ingest a single document"""
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}", "file_name": file_name}
        
        if not self._is_supported_file(file_path):
            return {"status": "error", "message": f"Unsupported file type: {Path(file_path).suffix}", "file_name": file_name}
        
        logger.info(f"Starting ingestion of {file_name}")
        
        try:
            # Extract text
            text = self.document_processor.extract_text(file_path)
            if not text.strip():
                return {"status": "warning", "message": f"No text content extracted from {file_name}", "file_name": file_name}
            
            # Split into chunks
            chunks = self.text_splitter.split_text(text)
            if not chunks:
                return {"status": "warning", "message": f"No text chunks created from {file_name}", "file_name": file_name}
            
            # Prepare metadata
            doc_type = self.document_processor.get_document_type(file_path)
            metadatas = [
                {
                    "source": file_name, 
                    "chunk": i+1, 
                    "total_chunks": len(chunks), 
                    "document_type": doc_type, 
                    "file_path": file_path, 
                    "chunk_size": len(chunk)
                } 
                for i, chunk in enumerate(chunks)
            ]
            ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]
            
            # Add to vector database
            self.vector_db_client.add_documents(documents=chunks, metadatas=metadatas, ids=ids)
            
            logger.info(f"Successfully ingested {file_name} with {len(chunks)} chunks")
            return {
                "status": "success", 
                "message": f"Document {file_name} ingested successfully", 
                "file_name": file_name, 
                "chunks_created": len(chunks), 
                "document_type": doc_type, 
                "embedding_provider": self.provider
            }
            
        except Exception as e:
            logger.error(f"Error ingesting {file_name}: {e}")
            return {"status": "error", "message": f"Failed to ingest document: {str(e)}", "file_name": file_name}

    async def ingest_directory(self, directory_path: str) -> Dict[str, Any]:
        """Ingest all supported documents in a directory"""
        if not os.path.exists(directory_path):
            return {"status": "error", "message": f"Directory not found: {directory_path}"}
        
        results = {
            "total_files": 0, 
            "successful": 0, 
            "failed": 0, 
            "warnings": 0, 
            "skipped": 0, 
            "details": []
        }
        
        logger.info(f"Starting directory ingestion from {directory_path}")
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if not os.path.isfile(file_path):
                continue
                
            results["total_files"] += 1
            
            if not self._is_supported_file(file_path):
                logger.info(f"Skipping unsupported file: {filename}")
                results["skipped"] += 1
                results["details"].append({
                    "file_name": filename, 
                    "status": "skipped", 
                    "message": f"Unsupported file type: {Path(file_path).suffix}"
                })
                continue
            
            result = await self.ingest_document(file_path, filename)
            results["details"].append(result)
            
            if result["status"] == "success":
                results["successful"] += 1
            elif result["status"] == "warning":
                results["warnings"] += 1
            else:
                results["failed"] += 1
        
        logger.info(f"Directory ingestion completed. Total: {results['total_files']}, "
                   f"Success: {results['successful']}, Failed: {results['failed']}, "
                   f"Warnings: {results['warnings']}, Skipped: {results['skipped']}")
        
        return results