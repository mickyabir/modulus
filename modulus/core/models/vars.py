# modulus/core/models/vars.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class VarsConfig:
    values: Dict[str, str]