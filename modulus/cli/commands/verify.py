from modulus.core.parser import TomlParser

def verify_llm(resource_type, config):
    return True

def verify_memory(resource_type, config):
    return True

def verify_tool(resource_type, config):
    resources = config.get(resource_type)

    if resources is None:
        return True

    for resource_name in resources:
        resource = resources.get(resource_name)

        if resource.type not in ["function", "api", "vector_lookup"]:
            print(f"Tool '{resource_name}' references unavailable type '{resource.type}'")
            return False

        memory = resource.params.get("memory")

        if memory is not None:
            if config.get("memory").get(memory) is None:
                print(f"Tool '{resource_name}' references non-existent memory '{memory}'")
                return False

    return True

def verify_agent(resource_type, config):
    resources = config.get(resource_type)

    if resources is None:
        return True

    for resource_name in resources:
        resource = resources.get(resource_name)

        llm = resource.llm

        if config.get("llm").get(llm) is None:
            print(f"Agent '{resource_name}' references non-existent LLM '{llm}'")
            return False

        tools = resource.tools

        for tool in tools:
            if config.get("tool").get(tool) is None:
                print(f"Agent '{resource_name}' references non-existent tool '{tool}'")
                return False

        memory = resource.memory

        if config.get("memory").get(memory) is None:
            print(f"Agent '{resource_name}' references non-existent memory '{memory}'")
            return False

    return True

def verify_task(resource_type, config):
    resources = config.get(resource_type)

    if resources is None:
        return True

    for resource_name in resources:
        resource = resources.get(resource_name)

        entry_agent = resource.entry_agent

        if config.get("agent").get(entry_agent) is None:
            print(f"Task '{resource_name}' references non-existent entry_agent '{entry_agent}'")
            return False

        handoff_to = resource.params.get("handoff_to")

        if handoff_to is not None:
            if config.get("agent").get(handoff_to) is None:
                print(f"Agent '{resource_name}' references non-existent handoff_to '{handoff_to}'")
                return False

def verify_deployment(resource_type, config):
    resources = config.get(resource_type)

    if resources is None:
        return True

    for resource_name in resources:
        resource = resources.get(resource_name)

        expose = resource.expose

        for task in expose:
            if config.get("task").get(task) is None:
                print(f"Deployment '{resource_name}' references non-existent expose task '{task}'")
                return False

def verify():
    config_file = "modulus.toml"
    parser = TomlParser()
    config = parser.parse(config_file)
    for resource_type, resources in config.items():
        if resource_type == "llm":
            verify_llm(resource_type, config)
        elif resource_type == "memory":
            verify_memory(resource_type, config)
        elif resource_type == "tool":
            verify_tool(resource_type, config)
        elif resource_type == "agent":
            verify_agent(resource_type, config)
        elif resource_type == "task":
            verify_task(resource_type, config)
        elif resource_type == "deployment":
            verify_deployment(resource_type, config)
