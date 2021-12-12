from models.reader import Reader


class TextReader(Reader):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name

    def read(self):
        with open(self.__file_name, 'r') as file:
            return file.read()
