from abc import abstractmethod, ABC


class Writer(ABC):
    """
    Abstract class for writing data to a file.
    """

    @abstractmethod
    def write(self, data):
        """
        Write data to a file.
        """
        pass
