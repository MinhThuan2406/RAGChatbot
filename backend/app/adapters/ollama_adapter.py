# backend/app/adapters/ollama_adapter.py
import httpx
from ..core.interfaces import AbstractLLMClient, AbstractEmbeddingClient

class OllamaAdapter(AbstractLLMClient, AbstractEmbeddingClient):
    def __init__(self, host: str, port: int):
        self.base_url = f"http://{host}:{port}/api"
        self.client = httpx.AsyncClient()
        self.model = "llama3"  # Use your actual Llama 3.2 model name here

    async def generate_response(self, prompt: str, context: str | None = None) -> str:
        full_prompt = f"Context: {context}\n\nQuestion: {prompt}" if context else prompt
        response = await self.client.post(
            f"{self.base_url}/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")

    async def create_embedding(self, text: str) -> list[float]:
        response = await self.client.post(
            f"{self.base_url}/embeddings",
            json={
                "model": self.model,  # Use Llama 3.2 for embeddings
                "prompt": text
            }
        )
        response.raise_for_status()
        return response.json().get("embedding", [])