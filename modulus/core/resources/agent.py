from modulus.core.resources.provider import Provider

class Agent:
    def __init__(self, name: str, provider: Provider, prompt: str = None):
        self.name = name
        self.provider = provider
        self.prompt = prompt

    def message(self, input_text: str, injected_prompt: str = None) -> str:
        full_input = input_text

        if self.prompt:
            full_input = f"{self.prompt}\n\nUser: {input_text}"

        if injected_prompt:
            full_input = f"{injected_prompt}\n\n{full_input}"

        return self.provider.query(full_input)
