from pathlib import Path
from tomlkit import parse
from typing import Callable, Type, TypeVar, Any, Dict, cast

from modulus.core.models import AgentConfig, DeploymentConfig, LLMConfig, MemoryConfig, EmbeddingConfig, TaskConfig, ToolConfig, VarsConfig, ProviderConfig

T = TypeVar('T')


def _get_required_opt_typed(
        block_type: str,
        block_name: str,
        opt_tag: str,
        block: Dict[str, Any],
        expected_type: Type[T]
) -> T:
    value = block.get(opt_tag)
    if value is None:
        raise ValueError(f"{block_type}.{block_name} is missing a '{opt_tag}'")

    if not isinstance(value, expected_type):
        raise ValueError(
            f"{block_type}.{block_name} has invalid type for '{opt_tag}': expected {expected_type.__name__}, got {type(value).__name__}"
        )

    return cast(T, value)


class TomlParser():
    def __init__(self) -> None:
        self.resource_parsers: Dict[str, Callable[[str, Dict[str, Any]], Any]] = {
            "agent": self.parse_agent_block,
            "deployment": self.parse_deployment_block,
            "embedding": self.parse_embedding_block,
            "llm": self.parse_llm_block,
            "memory": self.parse_memory_block,
            "provider": self.parse_provider_block,
            "task": self.parse_task_block,
            "tool": self.parse_tool_block,
            "vars": lambda name, block: self.parse_vars_block(block),
        }

    def parse_provider_block(self, name: str, block: Dict[str, Any]) -> ProviderConfig:
        """
        Parse a single [provider.<name>] block into an ProviderConfig instance.
        """
        provider_type: str = _get_required_opt_typed("provider", name, "type", block, str)

        api_key = block.get("api_key", None)
        known_keys = {"type", "api_key"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return ProviderConfig(
            name=name,
            type=provider_type,
            api_key=api_key,
            params=params
        )

    def parse_llm_block(self, name: str, block: Dict[str, Any]) -> LLMConfig:
        """
        Parse a single [llm.<name>] block into an LLMConfig instance.
        """
        provider: str = _get_required_opt_typed("llm", name, "provider", block, str)
        model: str = _get_required_opt_typed("llm", name, "model", block, str)

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

    def parse_embedding_block(self, name: str, block: Dict[str, Any]) -> EmbeddingConfig:
        """
        Parse a single [embedding.<name>] block into an EmbeddingConfig instance.
        """
        provider: str = _get_required_opt_typed("embedding", name, "provider", block, str)
        model: str = _get_required_opt_typed("embedding", name, "model", block, str)
        known_keys = {"provider", "model"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return EmbeddingConfig(
            name=name,
            provider=provider,
            model=model,
            params=params
        )

    def parse_memory_block(self, name: str, block: Dict[str, Any]) -> MemoryConfig:
        """
        Parse a single [memory.<name>] block into an MemoryConfig instance.
        """
        memory_type: str = _get_required_opt_typed("memory", name, "type", block, str)
        persist = block.get("persist", False)
        namespace = block.get("namespace")
        embedding = block.get("embedding")
        known_keys = {"type", "persist", "namespace", "embedding"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return MemoryConfig(
            name=name,
            type=memory_type,
            persist=persist,
            namespace=namespace,
            embedding=embedding,
            params=params
        )

    def parse_task_block(self, name: str, block: Dict[str, Any]) -> TaskConfig:
        """
        Parse a single [task.name] block into an TaskConfig instance.
        """
        description = block.get("description", "")
        flow: list[str] = _get_required_opt_typed("task", name, "flow", block, list)
        input_schema: Dict[str, str] = _get_required_opt_typed("task", name, "input_schema", block, dict)
        output_schema: Dict[str, str] = _get_required_opt_typed("task", name, "output_schema", block, dict)
        known_keys = {"description", "flow", "input_schema", "output_schema"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return TaskConfig(
            name=name,
            description=description,
            flow=flow,
            input_schema=input_schema,
            output_schema=output_schema,
            params=params
        )

    def parse_tool_block(self, name: str, block: Dict[str, Any]) -> ToolConfig:
        """
        Parse a single [tool.name] block into an ToolConfig instance.
        """
        tool_type: str = _get_required_opt_typed("tool", name, "type", block, str)
        known_keys = {"type"}
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
        prompt: str = _get_required_opt_typed("agent", name, "prompt", block, str)
        llm: str = _get_required_opt_typed("agent", name, "llm", block, str)
        tools: list[str] = _get_required_opt_typed("agent", name, "tools", block, list)
        memory: str = block.get("memory")

        known_keys = {"prompt", "llm", "tools", "memory"}
        params = {k: v for k, v in block.items() if k not in known_keys}

        return AgentConfig(
            name=name,
            prompt=prompt,
            llm=llm,
            tools=tools,
            memory=memory,
            params=params
        )

    def parse_deployment_block(self, name: str, block: Dict[str, Any]) -> DeploymentConfig:
        """
        Parse a single [tool.name] block into an ToolConfig instance.
        """
        runtime: str = _get_required_opt_typed("deployment", name, "runtime", block, str)
        expose: list[str] = _get_required_opt_typed("deployment", name, "expose", block, list)
        port: int = _get_required_opt_typed("deployment", name, "port", block, int)

        return DeploymentConfig(
            name=name,
            runtime=runtime,
            expose=expose,
            port=port,
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
                    "vars": parser_fn("", resource_blocks)
                }
            else:
                for resource_name, block in resource_blocks.items():
                    parsed_resources[resource_name] = parser_fn(resource_name, block)
                results[resource_type] = parsed_resources

        return results
