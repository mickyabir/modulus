import os
from modulus.core.parser import TomlParser
from modulus.core.util import flatten_resources
from modulus.core.resources.provider import Provider, OpenAIProvider
from modulus.core.resources.agent import Agent
from modulus.core.resources.task import Task

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


def create_provider_from_config(config: dict) -> Provider:
    provider_type = config.get("provider")
    if provider_type == "openai":
        return OpenAIProvider(config)
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")


def apply():
    parser = TomlParser()
    config_data = parser.parse(CONFIG_FILE)
    # config_resources = flatten_resources(config_data)
    #
    # if os.path.isfile(STATE_FILE):
    #     state_data = parser.parse(STATE_FILE)
    #     state_resources = flatten_resources(state_data)
    # else:
    #     state_resources = {}

    providers = {}
    for llm_name in config_data.get('llm'):
        llm = config_data.get('llm').get(llm_name)

        if llm.provider == 'openai':
            api_key = llm.api_key
            if llm.api_key and llm.api_key.startswith("@var:"):
                api_key_name = llm.api_key[len("@var:"):]
                api_key = config_data.get('vars').get('vars').values.get(api_key_name, None)
            elif llm.api_key and llm.api_key.startswith("@env:"):
                api_key = os.environ.get(llm.api_key[len('@env:')], None)

            main_params = {
                'temperature': llm.temperature, 'max_tokens': llm.max_tokens
            }
            providers[llm_name] = OpenAIProvider(llm.model, api_key, main_params | llm.params)
        else:
            raise f"Provider {llm.provider} is currently not supported"

    agents = {}
    for agent_name in config_data.get('agent'):
        agent_config = config_data.get('agent').get(agent_name)

        # Validate
        provider = providers.get(agent_config.llm)

        prompt = agent_config.prompt

        if prompt.startswith("@file:"):
            filename = prompt[len("@file:"):]
            with open(filename, 'r') as file:
                prompt = file.read()

        agents[agent_config.name] = Agent(agent_config.name, provider, prompt)

    tasks = {}
    for task_name in config_data.get('task'):
        task_config = config_data.get('task').get(task_name)

        task_agents_names = task_config.flow

        flow = [agents[agent_name] for agent_name in task_agents_names]

        tasks[task_name] = Task(task_name, flow, task_config.input_schema, task_config.output_schema)


    print(tasks['qa'].start("Teach me about topological qubits"))

    # agent = agents['researcher']
    # print(agent.message("Teach me about topological qubits"))
