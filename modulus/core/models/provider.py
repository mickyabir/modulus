from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class ProviderConfig:
    name: str
    type: str
    api_key: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
