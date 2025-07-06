from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DeploymentConfig:
    name: str
    runtime: str
    expose: List[str]
    port: int
