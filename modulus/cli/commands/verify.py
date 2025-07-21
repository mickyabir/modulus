import os

from modulus.core.parser import TomlParser


def verify_provider(resources, config):
    for resource, params in resources.items():
        # TODO: verify api_key exists if specified
        if params.type == 'openai':
            continue
        else:
            print(f"Provider `{params.provider}` support coming soon")
            return False

    return True


def verify_llm(resources, config):
    for resource_name in resources:
        resource = resources.get(resource_name)

        provider = resource.params.get("provider")

        if provider is not None:
            if config.get("provider").get(provider) is None:
                print(f"LLM '{resource_name}' references non-existent provider '{provider}'")
                return False

    return True


def verify_embedding(resources, config):
    for resource_name in resources:
        resource = resources.get(resource_name)

        provider = resource.params.get("provider")

        if provider is not None:
            if config.get("provider").get(provider) is None:
                print(f"Embedding '{resource_name}' references non-existent provider '{provider}'")
                return False

    return True


def verify_memory(resources, config):
    if resources is None:
        return True

    for resource_name in resources:
        resource = resources.get(resource_name)

        embedding = resource.params.get("embedding")

        if embedding is not None:
            if config.get("embedding").get(embedding) is None:
                print(f"Memory '{resource_name}' references non-existent embedding '{embedding}'")
                return False

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

        flow = resource.flow

        for agent in flow:
            if config.get("agent").get(agent) is None:
                print(f"Task '{resource_name}' references non-existent agent '{agent}'")
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
        elif resource_type == "embedding":
            verified = verified and verify_embedding(resources, config)
        elif resource_type == "tool":
            verified = verified and verify_tool(resources, config)
        elif resource_type == "agent":
            verified = verified and verify_agent(resources, config)
        elif resource_type == "task":
            verified = verified and verify_task(resources, config)
        elif resource_type == "deployment":
            verified = verified and verify_deployment(resources, config)
        elif resource_type == "provider":
            verified = verified and verify_provider(resources, config)

    if not verified:
        print("\nModulus config file is not valid")
    else:
        print("\nModulus config file is valid")
