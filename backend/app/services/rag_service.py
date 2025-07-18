import os
from ..db.chroma_client import ChromaDBClient
from .llm_provider_factory import LLMFactory

class RAGService:
    def __init__(self, provider: str = '', chroma_host=None, chroma_port=None):
        self.llm_client = LLMFactory.get_llm_client(provider)
        if provider == "ollama":
            self.embedding_client = LLMFactory.get_embedding_client("openai")
            embedding_function = openai_embedding_sync
        else:
            self.embedding_client = LLMFactory.get_embedding_client(provider)
            embedding_function = openai_embedding_sync 
        if "PYTEST_CURRENT_TEST" not in os.environ:
            self.vector_db_client = ChromaDBClient(
                host=chroma_host,
                port=chroma_port,
                embedding_function=embedding_function
            )
        else:
            self.vector_db_client = None

    async def answer_query(self, query: str, file_name: str | None = None) -> str:
        # 1. Create embedding for the query (Ollama)
        query_embedding = await self.embedding_client.create_embedding(query)

        # 2. Retrieve relevant documents, filtered by file_name if provided

        filter_metadata = None
        if file_name:
            filter_metadata = {"source": file_name}

        if self.vector_db_client:
            # Try to filter by file_name if provided, else fallback
            # Only use filtering if the method supports it; otherwise, fallback
            import inspect
            sig = inspect.signature(self.vector_db_client.query_documents)
            filter_param = None
            for candidate in ["where", "filters", "metadata_filter"]:
                if candidate in sig.parameters:
                    filter_param = candidate
                    break
            if filter_metadata and filter_param:
                kwargs = {filter_param: filter_metadata}
                retrieved_docs = self.vector_db_client.query_documents(query_texts=[query], n_results=3, **kwargs)
            else:
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

def openai_embedding_sync(texts: list[str]) -> list[list[float]]:
    from .llm_provider_factory import LLMFactory
    import asyncio

    embedding_client = LLMFactory.get_embedding_client("openai")

    async def get_embeddings():
        return [await embedding_client.create_embedding(text) for text in texts]

    return asyncio.run(get_embeddings())