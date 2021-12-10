from typing import List

from models.definer import Definer, NotFoundException, DefinerStorage
from models.word import WordDefinition


class MultiSourceDefinerWithStorage(Definer):
    def __init__(self, storage: DefinerStorage, definers: List[Definer]):
        self.__storage = storage
        self.__definers = definers

    def define(self, word) -> List[WordDefinition]:
        if self.__storage.exists(word):
            return self.__storage.define(word)

        for definer in self.__definers:
            try:
                definition = definer.define(word)
                if definition is not None:
                    self.__storage.store(word, definition)
                    return definition
            except NotFoundException:
                continue

        raise NotFoundException("word {} not found in any source".format(word))
