import chromadb
from ..core.config import settings

class ChromaDBClient:
    def __init__(self, host=None, port=None):
        # Delay client and collection creation until needed
        self._host = host or settings.CHROMA_HOST
        self._port = port or settings.CHROMA_PORT
        self._client = None
        self._collection = None

    @property
    def client(self):
        if self._client is None:
            self._client = chromadb.HttpClient(host=self._host, port=self._port)
        return self._client

    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(name="rag_documents")
        return self._collection

    def add_documents(self, documents: list, metadatas: list, ids: list):
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def query_documents(self, query_texts: list, n_results: int = 5):
        return self.collection.query(query_texts=query_texts, n_results=n_results)

# Only export the class, not an instance
__all__ = ["ChromaDBClient"]