from typing import List
from modulus.core.resources.task import Task
from abc import ABC, abstractmethod


class DeploymentRuntime(ABC):
    @abstractmethod
    def start(self, tasks: List[Task], port: int):
        pass


class Deployment:
    def __init__(self, name: str, expose: List[Task], port: int, runtime: DeploymentRuntime):
        self.name = name
        self.expose = expose
        self.port = port
        self.runtime = runtime

    def start(self):
        print(f"[modulus] Starting deployment: {self.name} on port {self.port}")
        self.runtime.start(self.expose, self.port)
