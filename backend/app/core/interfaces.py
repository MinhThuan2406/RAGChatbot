# backend/app/core/interfaces.py

from abc import ABC, abstractmethod

class AbstractLLMClient(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass

class AbstractEmbeddingClient(ABC):
    @abstractmethod
    async def create_embedding(self, text: str) -> list[float]:
        pass
