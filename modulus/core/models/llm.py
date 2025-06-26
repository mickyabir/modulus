from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class LLMConfig:
    name: str                      # Unique name/ID of the LLM resource
    provider: str                  # e.g. "openai", "anthropic"
    model: str                    # Model name, e.g. "gpt-4o", "claude-3"
    temperature: float = 0.7       # Sampling temperature
    max_tokens: Optional[int] = None  # Optional max tokens
    params: Dict[str, any] = field(default_factory=dict)  # Extra provider-specific params
