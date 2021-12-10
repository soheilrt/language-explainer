import os.path
import pickle
from typing import List

from models.definer import DefinerStorage, NotFoundException
from models.word import WordDefinition


class JsonDefinerStorage(DefinerStorage):
    def exists(self, word: str) -> bool:
        return os.path.exists(self.__get_word_store_location(word))

    def __init__(self):
        self.__storage_location = os.path.join(os.path.dirname(__file__), '../data/definitions')

        if not os.path.exists(self.__storage_location):
            os.makedirs(self.__storage_location)

    def store(self, word: str, definitions: List[WordDefinition]):
        with open(self.__get_word_store_location(word), 'wb') as f:
            pickle.dump(definitions, f)

    def define(self, word) -> List[WordDefinition]:
        word_location = self.__get_word_store_location(word)

        if not self.exists(word):
            raise NotFoundException(f"Word {word} not found")

        with open(word_location, 'rb') as f:
            return pickle.load(f)

    def __get_word_store_location(self, word: str):
        return os.path.join(self.__storage_location, f"{word}.bin")
