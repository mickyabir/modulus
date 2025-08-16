import json

from modulus.core.resources.agent import Agent


class Task:
    def __init__(self, name: str, flow: list[Agent], input_schema: dict, output_schema: dict,
                 output_intermediate: bool):
        self.name = name
        self.flow = flow
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.output_intermediate = output_intermediate

    def start(self, input_text: str) -> str:
        current_text = input_text
        num_agents = len(self.flow)

        return_text = ""

        for i, agent in enumerate(self.flow):
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

            if self.output_intermediate:
                return_text += f"AGENT: {agent.name}\n"
                return_text += f"MODEL: {agent.llm.get_model()}\n\n"
                return_text += current_text
                return_text += "\n\n"

        if self.output_intermediate:
            return return_text

        return current_text
