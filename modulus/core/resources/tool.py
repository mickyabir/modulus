from abc import ABC, abstractmethod
from typing import Callable


def function(description: str):
    def decorator(fn):
        fn._tool_description = description
        return fn
    return decorator

class Tool(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, kwargs: dict[str, str]) -> str:
        pass


class Function(Tool):
    def __init__(self, name: str, fn: Callable):
        super().__init__(name)
        self.fn = fn

    def run(self, kwargs: dict[str, str]) -> str:
        return self.fn(*kwargs)
