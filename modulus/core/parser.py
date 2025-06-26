# modulus/core/parser.py

from pathlib import Path
from tomlkit import parse
from typing import Dict, Any, Callable

from modulus.core.models.llm import LLMConfig
from modulus.core.models.memory import MemoryConfig

class TomlParser():
    def __init__(self):
        self.RESOURCE_PARSERS: Dict[str, Callable[[str, Dict[str, Any]], Any]] = {
            "llm": self.parse_llm_block,
            "memory": self.parse_memory_block,
            # "tool": parse_tool_block,
            # "agent": parse_agent_block,
        }

    def parse_llm_block(self, name: str, block: Dict[str, Any]) -> LLMConfig:
        """
        Parse a single [llm.<name>] block into an LLMConfig instance.
        """
        provider = block.get("provider")
        model = block.get("model")
        temperature = block.get("temperature", 0.7)
        max_tokens = block.get("max_tokens")
        known_keys = {"provider", "model", "temperature", "max_tokens"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return LLMConfig(
            name=name,
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            params=params
        )

    def parse_memory_block(self, name: str, block: Dict[str, Any]) -> MemoryConfig:
        """
        Parse a single [memory.<name>] block into an MemoryConfig instance.
        """
        memory_type = block.get("type")
        persist = block.get("persist", False)
        namespace = block.get("namespace")
        embedding_model = block.get("embedding_model")

        return MemoryConfig(
            name=name,
            type=memory_type,
            persist=persist,
            namespace=namespace,
            embedding_model=embedding_model
        )


    # Add other parse functions here, e.g.:
    # def parse_tool_block(...)
    # def parse_agent_block(...)

    def parse(self, toml_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse the TOML file and dispatch to resource-specific parsers.
        Returns a dict of resource type -> dict of resource name -> resource instance.
        Example:
        {
            "llm": {
                "default": LLMConfig(...),
                "retriever": LLMConfig(...)
            },
            "tool": {
                ...
            }
        }
        """
        toml_content = Path(toml_path).read_text(encoding="utf-8")
        doc = parse(toml_content)

        results = {}

        # Iterate top-level keys in the TOML document
        for resource_type, resource_blocks in doc.items():
            if resource_type not in self.RESOURCE_PARSERS:
                # Skip unknown resource types or handle them differently
                continue

            parser_fn = self.RESOURCE_PARSERS[resource_type]
            parsed_resources = {}

            # resource_blocks is a table of tables, e.g. [llm.default], [llm.retriever]
            for resource_name, block in resource_blocks.items():
                parsed_resources[resource_name] = parser_fn(resource_name, block)

            results[resource_type] = parsed_resources

        return results
