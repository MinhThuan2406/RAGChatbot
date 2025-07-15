import httpx
from ..core.interfaces import AbstractLLMClient, AbstractEmbeddingClient

class OllamaAdapter(AbstractLLMClient, AbstractEmbeddingClient):
    """
    Adapter for interacting with the Ollama LLM and embedding API.
    Implements both LLM and embedding client interfaces.
    """
    def __init__(self, host: str, port: int) -> None:
        """
        Args:
            host (str): Hostname or IP address of the Ollama server.
            port (int): Port number of the Ollama server.
        """
        self.base_url: str = f"http://{host}:{port}/api"
        self.client: httpx.AsyncClient = httpx.AsyncClient()
        self.model: str = "llama3.2:latest" 

    async def generate_response(self, prompt: str, context: str | None = None) -> str:
        """
        Generate a response from the LLM given a prompt and optional context.
        """
        full_prompt: str = f"Context: {context}\n\nQuestion: {prompt}" if context else prompt
        response = await self.client.post(
            f"{self.base_url}/chat",  
            json={
                "model": self.model,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")

    # async def create_embedding(self, text: str) -> list[float]:
    #     """
    #     Create an embedding for the given text using the Ollama API.

    #     Args:
    #         text (str): The input text to embed.

    #     Returns:
    #         list[float]: The embedding vector.
    #     """
    #     response = await self.client.post(
    #         f"{self.base_url}/embeddings",
    #         json={
    #     # Use Llama 3.2 for embeddings
    #             "prompt": text
    #         }
    #     )
    #     response.raise_for_status()
    #     return response.json().get("embedding", [])

    async def create_embedding(self, text: str) -> list[float]:
        """
        Ollama does not support embeddings via API.
        """
        raise NotImplementedError("Ollama does not provide an /api/embeddings endpoint. Use OpenAI or another provider for embeddings.")