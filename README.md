# Modulus

Modulus is a declarative framework for orchestrating AI infrastructure. It provides a simple, modular way to define, run, and deploy LLMs, agents, tools, and memory using a single `modulus.toml` configuration file.

Inspired by infrastructure-as-code tools like Terraform, Modulus brings the same declarative control to the world of large language models and intelligent systems.

## Overview

Modulus aims to answer the question: _What if defining and running LLM-based systems was as simple and composable as cloud infrastructure?_ With Modulus, you can:

- Define your LLMs, agents, tasks, and tools in TOML
- Compose flows using tasks powered by one or more agents
- Expose your agents and flows as web APIs using FastAPI
- Extend behavior by loading Python functions as tools
- (Coming soon) Store and query vector-based memory

Modulus is ideal for developers who want fine-grained, declarative control over LLM applications without having to write glue code for every new configuration.

## Installation

Modulus is a Python package and can be installed in editable mode during development:

```bash
git clone https://github.com/yourusername/modulus.git
cd modulus
uv pip install -e .
```

You can also use `pip` if you don't use `uv`.

## Quickstart

1. Create a `modulus.toml` file:

```toml
[vars]
[vars.values]
OPENAI_API_KEY = "@env:OPENAI_API_KEY"

[llm.default]
provider = "openai"
model = "gpt-4o"
api_key = "@var:OPENAI_API_KEY"
temperature = 0.7
max_tokens = 1024

[agent.qa]
llm = "default"
name = "qa"
prompt = "@file:prompts/qa.txt"

[task.qa_task]
flow = ["qa"]
input_schema = "string"
output_schema = "string"

[deployment.default]
runtime = "fastapi"
port = 8000
expose = ["task.qa_task"]
```

2. Create a prompt file:

```
prompts/qa.txt
```

```txt
Answer the user's question clearly and concisely.
```

3. Run the deployment:

```bash
modulus run
```

This will start a FastAPI server at `http://localhost:8000` with the QA task available as an endpoint.

## Core Concepts

### Providers

Providers manage access to APIs like OpenAI. They are defined once and referenced by LLMs and embedding models.

### LLMs

LLMs are defined by a provider, a model, and parameters like temperature and max tokens. These configurations are reusable across agents.

### Agents

An agent is a pairing of a prompt and an LLM. It is responsible for generating responses given a prompt and input. Agents can use tools and memory to behave more autonomously.

### Tasks

A task is a flow of one or more agents. Tasks define an input and output schema and are used as deployable units.

### Deployments

Deployments expose tasks via a runtime like FastAPI. They control how and where your intelligent system runs.

### Tools

Modulus allows you to register your own Python functions as tools, glue together API calls, or provide any outside functionality to agents. Tools can be invoked by agents or other logic in your flows.

Example:

```toml
[tool.greet]
type = "function"
function = "functions.tools.greet"
```

```python
# functions/tools.py

from modulus.core.decorator import tool_description

@tool_description("Greets the user with a message")
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

Modulus will introspect the function and make it callable as part of your flow.

## Memory

Modulus supports vector memory backends. You can define memory blocks that store and retrieve context using embeddings.

Example:

```toml
[embedding.ada]
provider = "openai"
model = "text-embedding-ada-002"

[memory.local]
embedding = "ada"
backend = "faiss"
path = "./memory/index.faiss"
```

This allows agents to recall previous interactions, build up context, and interact with stored knowledge over time.

## Directory Layout

A typical Modulus project might look like this:

```
.
├── modulus.toml
├── prompts/
│   └── qa.txt
├── functions/
│   └── tools.py
├── memory/
│   └── index.faiss (if using vector memory)
```

You can keep your logic, prompts, and configuration all in a clean, modular structure.

## Design Philosophy

- **Declarative**: Define what your system should do, not how it should do it.
- **Composable**: Combine building blocks like LLMs, agents, and tools into flexible pipelines.
- **Transparent**: No hidden behavior. What you configure is exactly what runs.
- **Source-first**: You own your code and your infrastructure.

## Roadmap

- [x] LLM and provider abstraction
- [x] Agent and task flows
- [x] FastAPI-based deployments
- [x] Custom tool loading with type and description extraction
- [ ] Vector memory support
- [ ] Streaming message support
- [ ] CLI diff and apply workflow
- [ ] Remote deployments and environments
- [ ] Web UI for visualization

## License

Modulus is licensed under the **Mozilla Public License 2.0 (MPL 2.0)**.

This means:

- You are free to use, modify, and redistribute Modulus under the terms of the MPL.
- Any changes made to existing MPL-licensed files must be shared under the same license.
- You are free to license new files you create, as long as they are separate from MPL-covered files.

See [LICENSE](./LICENSE) for the full license text.

## Contributing

Modulus is in active development. If you’re interested in contributing:

- Fork the repo
- Create a branch for your feature or fix
- Submit a pull request with context and reasoning

Contributions to documentation, examples, and testing are also very welcome.

## Inspiration

Modulus is inspired by Terraform (for declarative IaC) and LangChain (for tool and agent orchestration).

## Get Involved

Modulus is still in its early stages, and your feedback is extremely valuable. If you're building intelligent systems and want more control over how you define and deploy them, we’d love for you to try Modulus and share your thoughts.

```bash
git clone https://github.com/yourusername/modulus.git
cd modulus
modulus run
```

Follow the repo for updates, join discussions, or open issues with ideas and feature requests.

Modulus is your declarative AI infrastructure toolkit. Build with precision. Deploy with confidence.
