import numpy as np

from typing import List, Any

from modulus.core.resources.memory import Memory
from modulus.core.resources.embedding import EmbeddingModel


class LocalMemory(Memory):
    def __init__(self, embedder: EmbeddingModel):
        self.embedder = embedder
        self.data = []
        self.embeddings = []

    def add(self, text: str, metadata: dict = None):
        if metadata is None:
            metadata = {}

        embedding = self.embedder.embed(text)
        self.data.append((text, metadata))
        self.embeddings.append(np.array(embedding))

    def query(self, text: str, k: int = 5) -> List[Any]:
        if not self.embeddings:
            return []

        query_vec = np.array(self.embedder.embed(text))
        scores = [np.dot(query_vec, emb) for emb in self.embeddings]
        top_indices = np.argsort(scores)[::-1][:k]
        return [self.data[i] for i in top_indices]
