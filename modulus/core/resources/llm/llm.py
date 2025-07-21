from abc import ABC, abstractmethod

from openai import NOT_GIVEN

from modulus.core.resources.provider import OpenAIProvider
from modulus.core.resources.provider import Provider

class LLM(ABC):
    def __init__(self, provider: Provider, model: str, params: dict = {}):
        pass

    @abstractmethod
    def query(self, prompt: str):
        """Send a prompt and get a response."""
        pass


class OpenAILLM(LLM):
    def __init__(self, provider: OpenAIProvider, model: str, params: dict = {}):
        super().__init__()

        self.model = model
        self.provider = provider
        self.params = params

    def query(self, prompt: str) -> str:
        response = self.provider.get_client().responses.create(
            input=prompt,
            model=self.model,
            temperature=self.params.get('temperature', NOT_GIVEN),
            max_output_tokens=self.params.get('max_tokens', NOT_GIVEN),
            top_p=self.params.get('top_p', NOT_GIVEN),
        )

        return response.output_text

