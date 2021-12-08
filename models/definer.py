from abc import ABC, abstractmethod
from typing import List

from models.word import WordDefinition


class NotFoundException(Exception):
    pass


class Definer(ABC):
    @abstractmethod
    def define(self, word) -> List[WordDefinition]:
        pass
