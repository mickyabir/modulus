from abc import ABC, abstractmethod
from typing import List, Any


class Memory(ABC):
    @abstractmethod
    def add(self, text: str, metadata: dict = None) -> None:
        pass

    @abstractmethod
    def query(self, text: str, k: int = 5) -> List[Any]:
        pass
