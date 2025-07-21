import chromadb
import traceback
from typing import List, Optional, Any, Dict
from ..core.config import settings

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
            embedding_function: Embedding function object for generating embeddings.
        """
        self._host = host or settings.CHROMA_HOST
        self._port = port or settings.CHROMA_PORT
        self._client = None
        self._collection = None
        if isinstance(embedding_function, str):
            raise ValueError("embedding_function must be an instance of EmbeddingFunction, not a string")
        self._embedding_function = embedding_function
        print(f"[DEBUG] ChromaDBClient initialized with embedding_function type: {type(self._embedding_function)}")

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
            if self._embedding_function is not None and hasattr(self._embedding_function, "name"):
                print(f"[DEBUG] Embedding function name: {self._embedding_function.name()}")
            else:
                print(f"[DEBUG] Embedding function is None or has no 'name' attribute.")
            self._collection = self.client.get_or_create_collection(
                name="rag_documents",
                embedding_function=self._embedding_function
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
        print(f"[DEBUG] ChromaDBClient.add_documents called with {len(documents)} documents.")
        print(f"[DEBUG] First document: {documents[0][:200] if documents else 'N/A'}")
        print(f"[DEBUG] First metadata: {metadatas[0] if metadatas else 'N/A'}")
        print(f"[DEBUG] First id: {ids[0] if ids else 'N/A'}")
        try:
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        except Exception as e:
            print(f"[ERROR] Exception in add_documents: {e}")
            traceback.print_exc()
            raise

    def query_documents(self, query_texts: List[str], n_results: int = 5, **kwargs) -> Any:
        """
        Query the ChromaDB collection for relevant documents.
        Args:
            query_texts (List[str]): List of query strings.
            n_results (int): Number of results to return.
        Returns:
            Any: Query result from ChromaDB.
        """
        print(f"[DEBUG] ChromaDBClient.query_documents called with query_texts: {query_texts}, n_results: {n_results}, kwargs: {kwargs}")
        result = self.collection.query(query_texts=query_texts, n_results=n_results, **kwargs)
        print(f"[DEBUG] ChromaDBClient.query_documents result: {result}")
        return result

__all__ = ["ChromaDBClient"]