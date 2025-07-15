import os
from typing import Optional, Dict, Any, List
from ..db.chroma_client import ChromaDBClient
from .llm_provider_factory import LLMFactory
from pdfminer.high_level import extract_text
from langchain.text_splitter import RecursiveCharacterTextSplitter

class IngestionService:
    """
    Service for ingesting documents into the vector database (ChromaDB).
    Handles document loading, splitting, embedding, and storage.
    """
    def __init__(self, embedding_provider: str = "ollima", chroma_host: Optional[str] = None, chroma_port: Optional[int] = None) -> None:
        """
        Initialize the ingestion service.
        Args:
            embedding_provider (str): The embedding provider to use (default: "ollima").
            chroma_host (Optional[str]): Host for ChromaDB. Defaults to config.
            chroma_port (Optional[int]): Port for ChromaDB. Defaults to config.
        """
        self.embedding_client = LLMFactory.get_embedding_client()
        self.vector_db_client = ChromaDBClient(host=chroma_host, port=chroma_port)

    async def ingest_document(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """
        Ingest a document into the vector database.
        Loads a PDF, splits it into chunks, and stores embeddings in ChromaDB.
        Args:
            file_path (str): Path to the file to ingest.
            file_name (str): Name of the file.
        Returns:
            dict: Status and message about the ingestion.
        """

        # 1. Load PDF and extract text using pdfminer
        try:
            full_text = extract_text(file_path)
        except Exception as e:
            return {"status": "error", "message": f"Failed to load PDF: {e}"}

        # 2. Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks: list[str] = splitter.split_text(full_text)

        # 3. Prepare metadata and IDs
        metadatas: list[dict[str, Any]] = [{"source": file_name, "chunk": i+1} for i, _ in enumerate(chunks)]
        ids: list[str] = [f"{file_name}_chunk_{i}" for i, _ in enumerate(chunks)]

        # 4. Store in ChromaDB
        self.vector_db_client.add_documents(documents=chunks, metadatas=metadatas, ids=ids)
        return {"status": "success", "message": f"Document {file_name} ingested with {len(chunks)} chunks."}

# Only create the singleton instance if not running in test mode
if __name__ == "__main__" or "PYTEST_CURRENT_TEST" not in os.environ:
    ingestion_service: IngestionService = IngestionService()