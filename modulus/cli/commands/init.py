import os

example_config = """
# ============================
# Modulus TOML Schema v0.1
# ============================


# ----------------------------
# [llm.<name>]
# Defines a language model
# ----------------------------
[llm.default]
provider = "openai"                # required: "openai", "anthropic", etc.
model = "gpt-4o"                   # required
api_key = "@var:OPENAI_API_KEY_DEFAULT"
temperature = 0.7                  # optional, default = 0.7
max_tokens = 2048                 # optional

[llm.fast]
provider = "openai"
model = "gpt-3.5-turbo"
api_key = "@var:OPENAI_API_KEY_FAST"
temperature = 0.0


# ----------------------------
# [memory.<name>]
# Defines vector memory store
# ----------------------------
[memory.vectorstore]
type = "chroma"                    # required: chroma, weaviate, redis, etc.
persist = true                     # optional
namespace = "main"                 # optional
embedding_model = "text-embedding-ada-002"  # optional


# ----------------------------
# [[tool]]
# External API, function, or memory lookup
# ----------------------------
[tool.search]
type = "api"
endpoint = "https://api.serpapi.com/search"
method = "GET"
headers = { Authorization = "Bearer ${SERPAPI_KEY}" }

[tool.calculator]
type = "function"
command = "builtin:math.eval"

[tool.doc_lookup]
type = "vector_lookup"
memory = "vectorstore"

[tool.code_executor]
type = "function"
command = "builtin:code.run"  # Interpreted inside your runtime

# ----------------------------
# [[agent]]
# Defines an AI persona
# ----------------------------
[agent.researcher]
role = "Information seeker"
goal = "Find and summarize relevant data"
prompt = "@file:prompts/researcher.prompt"
llm = "default"
tools = ["search", "doc_lookup"]
memory = "vectorstore"

[agent.analyst]
role = "Data interpreter"
goal = "Analyze results and provide final output"
prompt = "@file:prompts/analyst.prompt"
llm = "fast"
tools = ["calculator"]
memory = "vectorstore"

[agent.coder]
role = "Python programmer"
goal = "Write working code to solve the given task"
prompt = "You are a coding agent."
llm = "default"
tools = ["code_executor", "search"]
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
expose = ["task.qa"]
port = 8080
auth_token = "${DEPLOY_AUTH_TOKEN}"

# ----------------------------
# [vars]
# Secrets and environment substitutions
# ----------------------------
[vars]
OPENAI_API_KEY_DEFAULT = "key"
OPENAI_API_KEY_FAST = "key"
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
