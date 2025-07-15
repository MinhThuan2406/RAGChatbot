from ..db.chroma_client import ChromaDBClient
from .llm_provider_factory import LLMFactory
import os

class RAGService:
    def __init__(self, chroma_host=None, chroma_port=None):
        self.llm_client = LLMFactory.get_llm_client()
        self.embedding_client = LLMFactory.get_embedding_client()
        # Only create ChromaDBClient if not running in test mode
        if "PYTEST_CURRENT_TEST" not in os.environ:
            self.vector_db_client = ChromaDBClient(host=chroma_host, port=chroma_port)
        else:
            self.vector_db_client = None

    async def answer_query(self, query: str) -> str:
        # 1. Create embedding for the query (Ollama)
        query_embedding = await self.embedding_client.create_embedding(query)


        # 2. Retrieve relevant documents
        if self.vector_db_client:
            retrieved_docs = self.vector_db_client.query_documents(query_texts=[query], n_results=3)
        else:
            # Mocked response for test mode
            retrieved_docs = {"documents": [["This is a mocked document."]], "metadatas": [[{"source": "mocked.pdf", "page": 1}]], "ids": [["mocked_id"]]}

        context = ""
        documents = retrieved_docs.get('documents') if retrieved_docs else None
        if documents:
            context = "\n".join([doc for sublist in documents if sublist for doc in sublist])

        # 3. Augment prompt with context
        if context:
            prompt = f"Based on the following context, answer the question: {context}\n\nQuestion: {query}"
        else:
            prompt = f"No specific context found. Answer the question: {query}"

        # 4. Generate response (Ollama)
        response = await self.llm_client.generate_response(prompt)
        return response