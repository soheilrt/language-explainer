from abc import ABC, abstractmethod
from typing import List


class Middleware(ABC):
    @abstractmethod
    def validate(self, data: List[str]) -> (List[str], int):
        pass
