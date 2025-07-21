from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class AgentConfig:
    name: str
    prompt: str
    llm: str
    tools: List[str]
    memory: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
