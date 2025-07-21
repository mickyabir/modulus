from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class EmbeddingConfig:
    name: str
    provider: str
    model: str
    params: Dict[str, Any] = field(default_factory=dict)
