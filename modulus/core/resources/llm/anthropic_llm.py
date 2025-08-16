from anthropic import NOT_GIVEN

from modulus.core.resources.provider import AnthropicProvider
from modulus.core.resources.llm import LLM


class AnthropicLLM(LLM):
    def __init__(self, provider: AnthropicProvider, model: str, params: dict = {}):
        super().__init__(provider, model, params)
        self.model = model
        self.provider = provider
        self.params = params

    def get_model(self):
        return self.model

    def query(self, prompt: str) -> str:
        temperature = self.params.get('temperature')
        if temperature is None:
            temperature = NOT_GIVEN

        max_tokens = self.params.get('max_tokens')
        if max_tokens is None:
            max_tokens = 1024

        response = self.provider.get_client().messages.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=self.params.get('top_p', NOT_GIVEN),
        )

        return response.content[0].text
