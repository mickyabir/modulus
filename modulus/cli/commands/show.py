from modulus.core.parser import TomlParser

def show():
    config_file = "modulus.toml"
    parser = TomlParser()
    config = parser.parse(config_file)

    for resource_type, resources in config.items():
        print(resource_type.upper())

        names = list(resources.keys())
        last_index = len(names) - 1

        for i, name in enumerate(names):
            resource = resources[name]
            is_last = (i == last_index)

            branch = "└─" if is_last else "├─"

            summary = summarize_resource(resource)

            print(f"{branch} {name} {summary}")

        print()


def summarize_resource(resource) -> str:
    if hasattr(resource, "provider") and hasattr(resource, "model"):
        return f"(provider={resource.provider}, model={resource.model})"
    if hasattr(resource, "type"):
        return f"(type={resource.type})"
    if hasattr(resource, "llm") and hasattr(resource, "tools") and hasattr(resource, "prompt"):
        tools_list = ", ".join(resource.tools) if resource.tools else ""
        return f"(llm={resource.llm}, prompt={resource.prompt}, tools=[{tools_list}])"
    if hasattr(resource, "description"):
        return f"({resource.description})"
    # Deployment special case
    if hasattr(resource, "port") and hasattr(resource, "expose") and hasattr(resource, "runtime"):
        expose_list = ", ".join(resource.expose) if resource.expose else ""
        return f"(port={resource.port}, tasks=[{expose_list}], runtime={resource.runtime})"
    return ""