from modulus.core.resources.provider import Provider

class Agent:
    def __init__(self, name: str, role: str, goal: str, provider: Provider, prompt: str = None):
        self.name = name
        self.role = role
        self.goal = goal
        self.provider = provider
        self.prompt = prompt

    def message(self, input_text: str) -> str:
        if self.prompt:
            full_input = f"{self.prompt}\n\nUser: {input_text}"
        else:
            full_input = input_text

        return self.provider.query(full_input)
