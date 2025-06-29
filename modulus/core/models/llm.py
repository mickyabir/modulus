from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class LLMConfig:
    name: str
    provider: str
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    params: Dict[str, Any] = field(default_factory=dict)
