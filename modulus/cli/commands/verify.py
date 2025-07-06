import os

from modulus.core.parser import TomlParser


def verify_llm(resources, config):
    for resource, params in resources.items():
        if params.provider == 'openai':
            continue
        else:
            print(f"Provider `{params.provider}` support coming soon")
            return False

    return True


def verify_memory(resources, config):
    return True


def verify_tool(resources, config):
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


def verify_prompt(prompt: str) -> bool:
    if prompt.startswith("@file:"):
        file_path = prompt[len("@file:"):]
        return os.path.isfile(file_path)
    return True


def verify_agent(resources, config):
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

        prompt = resource.prompt
        if not verify_prompt(prompt):
            print(f"Agent '{resource_name}' has invalid prompt: {prompt}")
            return False

    return True


def verify_task(resources, config):
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

    return True

def verify_deployment(resources, config):
    if resources is None:
        return True

    for resource_name in resources:
        resource = resources.get(resource_name)

        expose = resource.expose

        for task in expose:
            task = task.removeprefix("task.")
            if config.get("task").get(task) is None:
                print(f"Deployment '{resource_name}' references non-existent expose task '{task}'")
                return False

    return True

def verify():
    config_file = "modulus.toml"
    parser = TomlParser()
    config = parser.parse(config_file)
    verified = True
    for resource_type, resources in config.items():
        if resource_type == "llm":
            verified = verified and verify_llm(resources, config)
        elif resource_type == "memory":
            verified = verified and verify_memory(resources, config)
        elif resource_type == "tool":
            verified = verified and verify_tool(resources, config)
        elif resource_type == "agent":
            verified = verified and verify_agent(resources, config)
        elif resource_type == "task":
            verified = verified and verify_task(resources, config)
        elif resource_type == "deployment":
            verified = verified and verify_deployment(resources, config)

    if not verified:
        print("\nModulus config file is not valid")
    else:
        print("\nModulus config file is valid")
