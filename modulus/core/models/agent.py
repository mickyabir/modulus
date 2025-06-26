from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AgentConfig:
    name: str
    role: str
    goal: str
    llm: str
    tools: List[str]
    memory: str
    params: Dict[str, any] = field(default_factory=dict)
