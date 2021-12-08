from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def read(self) -> str:
        pass
