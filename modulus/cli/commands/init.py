import os

example_config = """
# ============================
# Modulus TOML Schema v0.1
# ============================

# ----------------------------
# [openai.<name>]
# Defines a model provider
# ----------------------------
[provider.openai]
type = "openai"
api_key = "@var:OPENAI_API_KEY"

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
role = "Information seeker"
goal = "Find and summarize relevant data"
prompt = "@file:prompts/researcher.prompt"
llm = "default"
tools = []
memory = "vectorstore"

[agent.analyst]
role = "Data interpreter"
goal = "Analyze results and provide final output"
prompt = "@file:prompts/analyst.prompt"
llm = "fast"
tools = []
memory = "vectorstore"

[agent.teacher]
role = "Information seeker"
goal = "Find and summarize relevant data"
prompt = "@file:prompts/teacher.prompt"
llm = "default"
tools = []
memory = "vectorstore"

[agent.simplifier]
role = "Simplifier"
goal = "Simplify results"
prompt = "@file:prompts/simplifier.prompt"
tools = ["foo"]
memory = "vectorstore"
llm = "fast"

[agent.coder]
role = "Python programmer"
goal = "Write working code to solve the given task"
prompt = "You are a coding agent."
llm = "default"
tools = []
memory = "vectorstore"
behavior = "loop"
loop_control = { max_steps = 10, stop_condition = "output.contains('SUCCESS')" }

# ----------------------------
# [task.<name>]
# Pipeline or multi-agent orchestration
# ----------------------------
[task.qa]
description = "Full question answering pipeline"
flow = ["researcher", "analyst"]
input_schema = { question = "string" }
output_schema = { answer = "string", citations = "array" }

[task.qa_simplified]
description = "Full question answering pipeline"
flow = ["researcher", "analyst", "simplifier"]
input_schema = { question = "string" }
output_schema = { answer = "string"}

[task.teaching]
description = "Full question answering pipeline"
flow = ["teacher"]
input_schema = { question = "string" }
output_schema = { lesson = "string", examples = "array", exercises = "array" }

[task.code_synthesis]
description = "Let the agent attempt to write working code"
flow = ["coder"]
input_schema = { problem = "string" }
output_schema = { solution = "string", logs = "array" }

# ----------------------------
# [deployment.<name>]
# Hosting configuration
# ----------------------------
[deployment.default]
runtime = "fastapi"
expose = ["task.teaching"]
port = 8080

# ----------------------------
# [vars]
# Secrets and environment substitutions
# ----------------------------
[vars]
OPENAI_API_KEY = "API_KEY"
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
