import json

from modulus.core.resources.agent import Agent

class Task:
    def __init__(self, name: str, flow: list[Agent], input_schema: dict, output_schema: dict):
        self.name = name
        self.flow = flow
        self.input_schema = input_schema
        self.output_schema = output_schema
    def start(self, input_text: str) -> str:
        current_text = input_text
        num_agents = len(self.flow)

        for i, agent in enumerate(self.flow):
            print(f"Task flow handed off to {agent.name}")
            if i == 0:
                current_text = agent.message(input_text)

            elif i == num_agents - 1:
                full_text = {
                    "previous_agent_output": current_text,
                    "original_input": input_text
                }

                if self.output_schema:
                    schema_str = json.dumps(self.output_schema, indent=2)
                    injected_prompt = (
                        f"Please structure your output to match the following schema:\n{schema_str}"
                    )
                else:
                    injected_prompt = ""

                current_text = agent.message(json.dumps(full_text), injected_prompt=injected_prompt)

            else:
                full_text = {
                    "previous_agent_output": current_text,
                    "original_input": input_text
                }
                current_text = agent.message(json.dumps(full_text))

        return current_text
