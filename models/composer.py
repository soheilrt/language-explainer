from abc import ABC, abstractmethod
from typing import List, Dict

from models.reader import Reader
from models.word import WordDefinition
from models.writer import Writer


class Composer(ABC):
    """
    Abstract class for composer.
    """

    @abstractmethod
    def compose(self, reader: Reader) -> Dict[str, List[WordDefinition]]:
        """
        Compose a message.
        """
        pass

    @abstractmethod
    def compose_write(self, reader: Reader, writer: Writer) -> None:
        """
        Compose and write to writer.
        :param reader: the object which reads the message.
        :param writer: the object which writes the message.
        """
        pass
