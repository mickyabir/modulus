import os

example_config = """# ============================
# Modulus TOML Schema v0.1
# ============================

# ----------------------------
# [openai.<name>]
# Defines a model provider
# ----------------------------
[provider.openai]
type = "openai"
api_key = "@var:OPENAI_API_KEY" # use @env:OPENAI_API_KEY if it is defined as an environment variable

# ----------------------------
# [llm.<name>]
# Defines a language model
# ----------------------------
[llm.default]
provider = "openai"
model = "gpt-4o"
temperature = 0.7
max_tokens = 2048

[llm.fast]
provider = "openai"
model = "gpt-3.5-turbo"
temperature = 0.0

# ----------------------------
# [embedding.<name>]
# Defines an embedding model
# ----------------------------
[embedding.ada]
provider = "openai"
model = "text-embedding-ada-002"

# ----------------------------
# [memory.<name>]
# Defines vector memory store
# ----------------------------
[memory.vectorstore]
type = "chroma"
persist = true
namespace = "main"
embedding_model = "text-embedding-ada-002"

# ----------------------------
# [[tool]]
# External API, function, or memory lookup
# ----------------------------
[tool.foo]
type = "function"
function = "functions/foo.foofn"

# ----------------------------
# [[agent]]
# Defines an AI persona
# ----------------------------
[agent.researcher]
prompt = "@file:prompts/researcher.prompt"
llm = "default"
tools = []
memory = "vectorstore"

[agent.analyst]
prompt = "@file:prompts/analyst.prompt"
llm = "fast"
tools = []
memory = "vectorstore"

# ----------------------------
# [task.<name>]
# Pipeline or multi-agent orchestration
# ----------------------------
[task.qa]
description = "Full question answering pipeline"
flow = ["researcher", "analyst"]
input_schema = { question = "string" }
output_schema = { answer = "string", citations = "array" }

# ----------------------------
# [deployment.<name>]
# Hosting configuration
# ----------------------------
[deployment.default]
runtime = "fastapi"
expose = ["task.qa"]
port = 8080

# ----------------------------
# [vars]
# Secrets and environment substitutions
# ----------------------------
[vars]
OPENAI_API_KEY = "API_KEY"
"""

example_function = """from modulus.core.resources.tool import function


@function("Returns true if x is even")
def foofn(x: int):
    return x % 2
"""

example_prompt_researcher = """You are a PhD level researcher.

You should be clear, concise, and professional in your responses.

Do not make information up, always give your evidence for claims, and make everything coherent.
"""

example_prompt_analyst = """You are a PhD level analyst.

Analyze the results and claims you are given, and provide your expert opinions based on facts and logic about what you have received.

Be clear and concise, and do not make anything up or hallucinate.

Use your best judgement and provide clear thoughts.
"""

def init(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

    config_filename = "modulus.toml"
    config_filepath = os.path.join(directory, config_filename)
    if os.path.isfile(config_filepath):
        print("Modulus is already initialized")
    else:
        with open(config_filepath, "w") as f:
            f.write(example_config)

    if not os.path.isdir("functions"):
        os.mkdir("functions")

    if not os.path.isdir("prompts"):
        os.mkdir("prompts")

    if not os.path.isfile("functions/foo.py"):
        with open("functions/foo.py", "w") as f:
            f.write(example_function)

    if not os.path.isfile("prompts/analyst.prompt"):
        with open("prompts/analyst.prompt", "w") as f:
            f.write(example_prompt_analyst)

    if not os.path.isfile("prompts/researcher.prompt"):
        with open("prompts/researcher.prompt", "w") as f:
            f.write(example_prompt_researcher)
