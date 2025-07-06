from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class AgentConfig:
    name: str
    role: str
    goal: str
    prompt: str
    llm: str
    tools: List[str]
    memory: str
    params: Dict[str, Any] = field(default_factory=dict)
