import os
import importlib
import inspect

from typing import Callable

from modulus.core.parser import TomlParser
from modulus.core.resources.provider import OpenAIProvider
from modulus.core.resources.agent import Agent
from modulus.core.resources.llm import OpenAILLM
from modulus.core.resources.task import Task
from modulus.core.resources.tool import Function
from modulus.core.resources.deployment import Deployment
from modulus.core.resources.runtime.fastapi_runtime import FastAPIRuntime
from modulus.core.resources.embedding import OpenAIEmbeddingModel

STATE_FILE = ".modulus.state.toml"
CONFIG_FILE = "modulus.toml"


def load_prompt(value: str) -> str:
    if value.startswith("@file:"):
        path = value[len("@file:"):]
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif os.path.isfile(value):
        return open(value, "r", encoding="utf-8").read()
    return value


def load_function(path: str):
    """
    Given a string like 'functions/foo.foofn', load and return the function object.
    Converts slashes to dots for module import.
    """
    # Replace slashes with dots to get module path + function name
    path = path.replace('/', '.')

    module_name, fn_name = path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    fn = getattr(module, fn_name)
    return fn


def get_function_signature(fn: Callable) -> str:
    """
    Return a string representation of the function's signature.
    """
    signature = inspect.signature(fn)
    return str(signature)


def run():
    parser = TomlParser()
    config_data = parser.parse(CONFIG_FILE)

    providers = {}
    for provider_name in config_data.get('provider'):
        provider = config_data.get('provider').get(provider_name)

        if provider.type == 'openai':
            api_key = provider.api_key
            if provider.api_key and provider.api_key.startswith("@var:"):
                api_key_name = provider.api_key[len("@var:"):]
                api_key = config_data.get('vars').get('vars').values.get(api_key_name, None)
            elif provider.api_key and provider.api_key.startswith("@env:"):
                api_key = os.environ.get(provider.api_key[len('@env:')], None)

            providers[provider_name] = OpenAIProvider(api_key, provider.params)
        else:
            raise NotImplementedError(f"Provider type {provider.type} is currently not supported")


    llms = {}
    for llm_name in config_data.get('llm'):
        llm = config_data.get('llm').get(llm_name)

        provider = providers.get(llm.provider)

        main_params = {
            'temperature': llm.temperature, 'max_tokens': llm.max_tokens
        }
        llms[llm_name] = OpenAILLM(provider, llm.model, main_params | llm.params)

    embeddings = {}
    for embedding_name in config_data.get('embedding'):
        embedding = config_data.get('embedding').get(embedding_name)

        provider = providers.get(embedding.provider)
        embeddings[embedding_name] = OpenAIEmbeddingModel(provider, embedding.model)

    tools = {}
    for tool_name in config_data.get('tool'):
        tool_config = config_data.get('tool').get(tool_name)

        if tool_config.type == 'function':
            function = tool_config.params.get('function')
            if function.startswith('@builtin:'):
                raise NotImplementedError(f"Tool {tool_name} calling builtin functions, not implemented")
            else:
                fn = load_function("functions/foo.foofn")
                tools[tool_name] = Function(tool_name, fn)
        else:
            raise NotImplementedError(f"Tool {tool_name} of type {tool_config.type} is not supported")

    agents = {}
    for agent_name in config_data.get('agent'):
        agent_config = config_data.get('agent').get(agent_name)

        # Validate
        llm = llms.get(agent_config.llm)

        prompt = agent_config.prompt

        if prompt.startswith("@file:"):
            filename = prompt[len("@file:"):]
            with open(filename, 'r') as file:
                prompt = file.read()

        agents[agent_config.name] = Agent(agent_config.name, llm, prompt)

    tasks = {}
    for task_name in config_data.get('task'):
        task_config = config_data.get('task').get(task_name)

        task_agents_names = task_config.flow

        flow = [agents[agent_name] for agent_name in task_agents_names]

        tasks[task_name] = Task(task_name, flow, task_config.input_schema, task_config.output_schema)

    deployments = {}
    for deployment_name in config_data.get('deployment'):
        deployment_config = config_data.get('deployment').get(deployment_name)

        expose = [tasks[task_name[len("task."):]] for task_name in deployment_config.expose]

        if deployment_config.runtime == 'fastapi':
            runtime = FastAPIRuntime()
        else:
            raise NotImplementedError(f"Unsupported deployment runtime `{deployment_config.runtime}`")

        deployments[deployment_name] = Deployment(deployment_name, expose, deployment_config.port, runtime)

    deployments['default'].start()

    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

    # print(tasks['qa_simplified'].start("Teach me about topological qubits"))
    # print(tools['foo'].run({}))
    # print(get_function_signature(tools['foo'].fn))
