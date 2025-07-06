from abc import ABC, abstractmethod
from openai import OpenAI, NOT_GIVEN


class Provider(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        """Establish connection or prepare client."""
        pass

    @abstractmethod
    def query(self, prompt: str):
        """Send a prompt and get a response."""
        pass


class OpenAIProvider(Provider):
    def __init__(self, model: str, api_key: str, params: dict = {}):
        super().__init__()

        self.api_key = api_key
        self.model = model
        self._client = None
        self.params = params

    def connect(self):
        self._client = OpenAI(api_key=self.api_key)

    def query(self, prompt: str) -> str:
        if self._client is None:
            self.connect()

        response = self._client.responses.create(
            input=prompt,
            model=self.model,
            temperature=self.params.get('temperature', NOT_GIVEN),
            max_output_tokens=self.params.get('max_tokens', NOT_GIVEN),
            top_p=self.params.get('top_p', NOT_GIVEN),
        )

        return response.output_text

