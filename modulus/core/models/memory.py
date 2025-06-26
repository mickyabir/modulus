from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoryConfig:
    name: str
    type: str
    persist: bool
    namespace: Optional[str] = None
    embedding_model: Optional[str] = None
