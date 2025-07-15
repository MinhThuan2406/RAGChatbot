import chromadb
from ..core.config import settings
from typing import List, Optional, Any, Dict

class ChromaDBClient:
    """
    Client for interacting with ChromaDB vector database.
    Handles connection, collection management, and document operations.
    """
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, embedding_function=None) -> None:
        """
        Args:
            host (Optional[str]): Hostname for ChromaDB. Defaults to settings.CHROMA_HOST.
            port (Optional[int]): Port for ChromaDB. Defaults to settings.CHROMA_PORT.
        """
        self._host: str = host or settings.CHROMA_HOST
        self._port: int = port or settings.CHROMA_PORT
        self._client: Optional[Any] = None
        self._collection: Optional[Any] = None
        self._embedding_function = embedding_function

    @property
    def client(self) -> Any:
        """Lazily initializes and returns the ChromaDB HTTP client."""
        if self._client is None:
            self._client = chromadb.HttpClient(host=self._host, port=self._port)
        return self._client

    @property
    def collection(self) -> Any:
        """Lazily initializes and returns the ChromaDB collection for RAG documents."""
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name="rag_documents",
                embedding_function=self._embedding_function  # <--- Pass it here!
            )
        return self._collection

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> None:
        """
        Add documents to the ChromaDB collection.
        Args:
            documents (List[str]): List of document texts.
            metadatas (List[Dict[str, Any]]): List of metadata dicts for each document.
            ids (List[str]): List of unique document IDs.
        """
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def query_documents(self, query_texts: List[str], n_results: int = 5) -> Any:
        """
        Query the ChromaDB collection for relevant documents.
        Args:
            query_texts (List[str]): List of query strings.
            n_results (int): Number of results to return.
        Returns:
            Any: Query result from ChromaDB.
        """
        return self.collection.query(query_texts=query_texts, n_results=n_results)

__all__ = ["ChromaDBClient"]