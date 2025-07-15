import os
# backend/app/services/ingestion_service.py
from ..db.chroma_client import ChromaDBClient
from.llm_provider_factory import LLMFactory
# from langchain_community.document_loaders import PyPDFLoader # Example loader
# from langchain_text_splitters import RecursiveCharacterTextSplitter # Example splitter


class IngestionService:
    def __init__(self, embedding_provider: str = "ollama", chroma_host=None, chroma_port=None):
        self.embedding_client = LLMFactory.get_embedding_client()
        # self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vector_db_client = ChromaDBClient(host=chroma_host, port=chroma_port)

    async def ingest_document(self, file_path: str, file_name: str):
        # 1. Load document (e.g., PDF)
        # loader = PyPDFLoader(file_path)
        # documents = loader.load()

        # For demonstration, let's use dummy content
        raw_content = f"This is content from {file_name}. It contains important information about the project. This is a second sentence."

        # 2. Split into chunks
        # chunks = self.text_splitter.split_documents(documents)
        chunks = [raw_content] # Simplified for demo

        texts = [chunk for chunk in chunks] # Extract text from chunks
        metadatas = [{"source": file_name, "page": i+1} for i, _ in enumerate(chunks)]
        ids = [f"{file_name}_chunk_{i}" for i, _ in enumerate(chunks)]

        # 3. Create embeddings for chunks
        # embeddings = [await self.embedding_client.create_embedding(text) for text in texts]
        # ChromaDB's add method can embed texts directly if you configure it with an embedding function
        # For this setup, we'll let ChromaDB handle embedding if it's configured, or pass texts directly.
        # If you want to pre-embed, you'd do:
        # embeddings = [await self.embedding_client.create_embedding(text) for text in texts]
        # chroma_client.add_documents(documents=texts, metadatas=metadatas, ids=ids, embeddings=embeddings)


        # For simplicity, let ChromaDB handle embedding internally if it's set up to do so
        self.vector_db_client.add_documents(documents=texts, metadatas=metadatas, ids=ids)
        return {"status": "success", "message": f"Document {file_name} ingested."}

# Only create the singleton instance if not running in test mode
if __name__ == "__main__" or "PYTEST_CURRENT_TEST" not in os.environ:
    ingestion_service = IngestionService()
  # Only create the singleton instance if not running in test mode
if __name__ == "__main__" or "PYTEST_CURRENT_TEST" not in os.environ:
    ingestion_service = IngestionService()