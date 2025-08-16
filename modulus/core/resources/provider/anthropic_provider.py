import anthropic

from modulus.core.resources.provider import Provider


class AnthropicProvider(Provider):
    def __init__(self, api_key: str, params: dict = {}):
        super().__init__()

        self.api_key = api_key
        self._client = None
        self.params = params

    def connect(self):
        super().connect()
        self._client = anthropic.Anthropic(api_key=self.api_key)

    def get_client(self):
        if self._client is None:
            self.connect()

        return self._client
