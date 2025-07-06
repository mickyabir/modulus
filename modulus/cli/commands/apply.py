import os
from modulus.core.parser import TomlParser
from modulus.core.util import flatten_resources
from modulus.core.resources.provider import Provider, OpenAIProvider
from modulus.core.resources.agent import Agent

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
    # parser = TomlParser()
    # config_data = parser.parse(CONFIG_FILE)
    # config_resources = flatten_resources(config_data)
    #
    # if os.path.isfile(STATE_FILE):
    #     state_data = parser.parse(STATE_FILE)
    #     state_resources = flatten_resources(state_data)
    # else:
    #     state_resources = {}

    provider = OpenAIProvider(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    agent = Agent(
        name="researcher",
        role="Information Seeker",
        goal="Find and summarize relevant data",
        provider=provider,
        prompt="You are a helpful AI researcher."
    )

    print(agent.message("Tell me about the Apollo mission."))

