from abc import ABC, abstractmethod


class Provider(ABC):
    def __init__(self):
        self.connected = False

    @abstractmethod
    def connect(self):
        self.connected = True

    def is_connected(self):
        return self.connected
