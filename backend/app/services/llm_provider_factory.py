# backend/app/services/llm_provider_factory.py
from ..core.config import settings
from ..core.interfaces import AbstractLLMClient, AbstractEmbeddingClient
# Import specific adapters
from..adapters.ollama_adapter import OllamaAdapter

class LLMFactory:
    @staticmethod
    def get_llm_client() -> AbstractLLMClient:
        # Only Ollama (Llama 3.2) is supported
        return OllamaAdapter(host=settings.OLLAMA_HOST, port=settings.OLLAMA_PORT)

    @staticmethod
    def get_embedding_client() -> AbstractEmbeddingClient:
        # Only Ollama (Llama 3.2) is supported
        return OllamaAdapter(host=settings.OLLAMA_HOST, port=settings.OLLAMA_PORT)