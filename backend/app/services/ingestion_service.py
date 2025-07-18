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
        Ingest a document (PDF, DOC, DOCX, image) into the vector database.
        Args:
            file_path (str): Path to the file to ingest.
            file_name (str): Name of the file.
        Returns:
            dict: Status and message about the ingestion.
        """
        import mimetypes
        import io
        ext = os.path.splitext(file_name)[1].lower()
        full_text = None

        if ext == ".pdf":
            try:
                full_text = extract_text(file_path)
            except Exception as e:
                return {"status": "error", "message": f"Failed to load PDF: {e}"}

        elif ext in [".doc", ".docx"]:
            try:
                if ext == ".docx":
                    import docx
                    doc = docx.Document(file_path)
                    full_text = "\n".join([para.text for para in doc.paragraphs])
                    extractor_used = "python-docx"
                else:
                    textract_exc = None
                    antiword_exc = None
                    catdoc_exc = None
                    extractor_used = None
                    # Try textract
                    try:
                        import textract
                        full_text = textract.process(file_path, timeout=30).decode("utf-8", errors="ignore")
                        extractor_used = "textract"
                    except Exception as e1:
                        textract_exc = e1
                    # Try antiword if textract failed
                    if (not full_text or not full_text.strip()) and extractor_used is None:
                        try:
                            import subprocess
                            result = subprocess.run(["antiword", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
                            if result.returncode == 0:
                                full_text = result.stdout.decode("utf-8", errors="ignore")
                                extractor_used = "antiword"
                            else:
                                antiword_exc = result.stderr.decode("utf-8", errors="ignore")
                        except Exception as e2:
                            antiword_exc = e2
                    # Try catdoc if antiword failed
                    if (not full_text or not full_text.strip()) and extractor_used is None:
                        try:
                            import subprocess
                            result2 = subprocess.run(["catdoc", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
                            if result2.returncode == 0:
                                full_text = result2.stdout.decode("utf-8", errors="ignore")
                                extractor_used = "catdoc"
                            else:
                                catdoc_exc = result2.stderr.decode("utf-8", errors="ignore")
                        except Exception as e3:
                            catdoc_exc = e3
                    if not full_text or not full_text.strip():
                        return {"status": "error", "message": f"Failed to load .doc file. textract: {textract_exc}, antiword: {antiword_exc}, catdoc: {catdoc_exc}"}
            except Exception as e:
                return {"status": "error", "message": f"Failed to load DOC/DOCX: {e}"}

        elif ext in [".jpg", ".jpeg", ".png"]:
            try:
                import pytesseract
                from PIL import Image
                image = Image.open(file_path)
                full_text = pytesseract.image_to_string(image)
            except Exception as e:
                return {"status": "error", "message": f"Failed to extract text from image: {e}"}
        else:
            return {"status": "error", "message": f"Unsupported file type: {ext}"}

        if not full_text or not full_text.strip():
            return {"status": "error", "message": "No text extracted from document."}

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks: list[str] = splitter.split_text(full_text)
        metadatas: list[dict[str, Any]] = [{"source": file_name, "chunk": i+1} for i, _ in enumerate(chunks)]
        ids: list[str] = [f"{file_name}_chunk_{i}" for i, _ in enumerate(chunks)]
        self.vector_db_client.add_documents(documents=chunks, metadatas=metadatas, ids=ids)
        return {"status": "success", "message": f"Document {file_name} ingested with {len(chunks)} chunks."}

    async def ingest_link(self, url: str) -> Dict[str, Any]:
        """
        Ingest a document from a URL (web page) into the vector database.
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            full_text = "\n".join([t for t in soup.stripped_strings])
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch or parse link: {e}"}

        if not full_text or not full_text.strip():
            return {"status": "error", "message": "No text extracted from link."}

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks: list[str] = splitter.split_text(full_text)
        metadatas: list[dict[str, Any]] = [{"source": url, "chunk": i+1} for i, _ in enumerate(chunks)]
        ids: list[str] = [f"{url}_chunk_{i}" for i, _ in enumerate(chunks)]
        self.vector_db_client.add_documents(documents=chunks, metadatas=metadatas, ids=ids)
        return {"status": "success", "message": f"Link {url} ingested with {len(chunks)} chunks."}

if __name__ == "__main__" or "PYTEST_CURRENT_TEST" not in os.environ:
    ingestion_service: IngestionService = IngestionService()