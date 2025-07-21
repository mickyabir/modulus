from abc import ABC, abstractmethod
from typing import List

from modulus.core.resources.provider import Provider

class EmbeddingModel(ABC):
    def __init__(self, provider: Provider, model_name: str):
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass
