from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TaskConfig:
    name: str
    description: str
    entry_agent: str
    input_schema: Dict[str, str]
    output_schema: Dict[str, str]
    params: Dict[str, any] = field(default_factory=dict)