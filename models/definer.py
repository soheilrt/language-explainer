from abc import ABC, abstractmethod
from typing import List

from models.word import WordDefinition


class NotFoundException(Exception):
    pass


class Definer(ABC):
    @abstractmethod
    def define(self, word) -> List[WordDefinition]:
        pass


class DefinerStorage(Definer, ABC):
    @abstractmethod
    def store(self, word: str, definitions: List[WordDefinition]):
        pass

    @abstractmethod
    def exists(self, word: str) -> bool:
        pass
