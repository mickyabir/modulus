from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ToolConfig:
    name: str
    type: str
    params: Dict[str, Any] = field(default_factory=dict)
