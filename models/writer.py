from abc import abstractmethod, ABC
from typing import List

from models.word import WordDefinition


class Writer(ABC):
    """
    Abstract class for writing data to a file.
    """

    @abstractmethod
    def write(self, data: List[WordDefinition]):
        """
        Write data to a file.
        """
        pass
