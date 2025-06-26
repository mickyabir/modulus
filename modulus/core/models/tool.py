from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ToolConfig:
    name: str
    type: str
    params: Dict[str, any] = field(default_factory=dict)
