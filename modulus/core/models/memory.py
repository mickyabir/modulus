from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class MemoryConfig:
    name: str
    type: str
    persist: bool
    namespace: Optional[str] = None
    embedding: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)