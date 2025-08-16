from modulus.core.resources.llm.llm import LLM
from modulus.core.resources.tool import Tool


class Agent:
    def __init__(self, name: str, llm: LLM, prompt: str = None, tools: dict[str, Tool] = None, max_iter=5):
        self.name = name
        self.llm = llm
        self.prompt = prompt
        self.tools = tools
        self.max_iter = max_iter

    def message(self, input_text: str, injected_prompt: str = None) -> str:
        full_input = input_text

        if self.prompt:
            full_input = f"{self.prompt}\n\nUser: {input_text}"

        if injected_prompt:
            full_input = f"{injected_prompt}\n\n{full_input}"

        return self.llm.query(full_input)
