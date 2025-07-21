from typing import List

from modulus.core.resources.embedding import EmbeddingModel
from modulus.core.resources.provider import OpenAIProvider


class OpenAIEmbeddingModel(EmbeddingModel):
    def __init__(self, provider: OpenAIProvider, model_name: str):
        super().__init__(provider, model_name)
        self.provider = provider
        self.model_name = model_name

    def embed(self, text: str) -> List[float]:
        response = self.provider.get_client().embeddings.create(
            model=self.model_name,
            input=text
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = self.provider.get_client().embeddings.create(
            model=self.model_name,
            input=texts
        )
        return [item.embedding for item in response.data]
