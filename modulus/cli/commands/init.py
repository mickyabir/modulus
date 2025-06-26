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
temperature = 0.2                  # optional, default = 0.7
max_tokens = 2048                 # optional
top_p = 0.9                        # optional provider-specific param
frequency_penalty = 0.5           # optional provider-specific param

[llm.fast]
provider = "openai"
model = "gpt-3.5-turbo"
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
llm = "default"
tools = ["search", "doc_lookup"]
memory = "vectorstore"

[agent.analyst]
role = "Data interpreter"
goal = "Analyze results and provide final output"
llm = "fast"
tools = ["calculator"]
memory = "vectorstore"

[agent.coder]
role = "Python programmer"
goal = "Write working code to solve the given task"
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
entry_agent = "researcher"
handoff_to = "analyst"
input_schema = { question = "string" }
output_schema = { answer = "string", citations = "array" }

[task.code_synthesis]
description = "Let the agent attempt to write working code"
entry_agent = "coder"
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
SERPAPI_KEY = "your-real-api-key"
DEPLOY_AUTH_TOKEN = "your-secret-token"
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
