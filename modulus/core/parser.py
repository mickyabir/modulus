# modulus/core/parser.py

from pathlib import Path
from tomlkit import parse
from typing import Dict, Any, Callable

from modulus.core.models.agent import AgentConfig
from modulus.core.models.deployment import DeploymentConfig
from modulus.core.models.llm import LLMConfig
from modulus.core.models.memory import MemoryConfig
from modulus.core.models.tool import ToolConfig
from modulus.core.models.vars import VarsConfig

class TomlParser():
    def __init__(self):
        self.resource_parsers: Dict[str, Callable[[str, Dict[str, Any]], Any]] = {
            "llm": self.parse_llm_block,
            "memory": self.parse_memory_block,
            "tool": self.parse_tool_block,
            "agent": self.parse_agent_block,
            "deployment": self.parse_deployment_block,
            "vars": self.parse_vars_block,
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

    def parse_tool_block(self, name: str, block: Dict[str, Any]) -> ToolConfig:
        """
        Parse a single [tool.name] block into an ToolConfig instance.
        """
        tool_type = block.get("type")
        known_keys = {"endpoint", "method", "headers", "command", "memory"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return ToolConfig(
            name=name,
            type=tool_type,
            params=params
        )

    def parse_agent_block(self, name: str, block: Dict[str, Any]) -> AgentConfig:
        """
        Parse a single [agent.name] block into an AgentConfig instance.
        """
        role = block.get("role")
        goal = block.get("goal")
        llm = block.get("llm")
        tools = block.get("tools")
        memory = block.get("memory")

        known_keys = {"endpoint", "method", "headers", "command", "memory"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return AgentConfig(
            name=name,
            role=role,
            goal=goal,
            llm=llm,
            tools=tools,
            memory=memory,
            params=params
        )

    def parse_deployment_block(self, name: str, block: Dict[str, Any]) -> DeploymentConfig:
        """
        Parse a single [tool.name] block into an ToolConfig instance.
        """
        runtime = block.get("runtime")
        expose = block.get("expose")
        port = block.get("port")
        auth_token = block.get("auth_token")

        return DeploymentConfig(
            name=name,
            runtime=runtime,
            expose=expose,
            port=port,
            auth_token=auth_token
        )

    def parse_vars_block(self, block: Dict[str, Any]) -> VarsConfig:
        """
        Parse the [vars] block (treated as a single-entry config).
        """
        return VarsConfig(values=dict(block))

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

        for resource_type, resource_blocks in doc.items():
            if resource_type not in self.resource_parsers:
                continue

            parser_fn = self.resource_parsers[resource_type]
            parsed_resources = {}

            if resource_type == "vars":
                results[resource_type] = {
                    "vars": parser_fn(resource_blocks)
                }
            else:
                for resource_name, block in resource_blocks.items():
                    parsed_resources[resource_name] = parser_fn(resource_name, block)
                results[resource_type] = parsed_resources


        return results
