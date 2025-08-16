from abc import ABC, abstractmethod

from modulus.core.resources.provider import Provider


class LLM(ABC):
    def __init__(self, provider: Provider, model: str, params: dict = None):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def query(self, prompt: str):
        """Send a prompt and get a response."""
        pass
