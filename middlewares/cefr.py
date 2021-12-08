import os
from typing import Union, Dict, List
import json

from models.middleware import Middleware


class CEFRLimiter(Middleware):
    """
     Validates that the CEFR level is within the specified range.
     """
    __CEFR_INPUT_TYPE = Union[str, int]

    class LEVELS:
        A1 = "A1"
        A2 = "A2"
        B1 = "B1"
        B2 = "B2"
        C1 = "C1"
        C2 = "C2"

    __UNKNOWN_LEVEL = "unknown"

    __LEVELS__ = {
        __UNKNOWN_LEVEL: -1,
        LEVELS.A1: 0,
        LEVELS.A2: 1,
        LEVELS.B1: 2,
        LEVELS.B2: 3,
        LEVELS.C1: 4,
        LEVELS.C2: 5,
    }

    def __init__(
            self,
            min_cefr: __CEFR_INPUT_TYPE = LEVELS.A1,
            max_cefr: __CEFR_INPUT_TYPE = LEVELS.C2,
            filter_unknowns: bool = False,
    ):
        """
        Initializes the validator.

        :param min_cefr: The minimum CEFR level.
        :param max_cefr: The maximum CEFR level.
        :param filter_unknowns: Whether to filter out unknown CEFR levels.
        """
        self.__filter_unknowns = filter_unknowns
        self.__words_data = self.__load_words_data()
        self.__min_cefr = self.__parse_cefr(min_cefr)
        self.__max_cefr = self.__parse_cefr(max_cefr)

    def __parse_cefr(self, cefr: __CEFR_INPUT_TYPE) -> int:
        if isinstance(cefr, int):
            return cefr
        elif isinstance(cefr, str):
            return self.__LEVELS__[cefr.upper()]
        else:
            raise ValueError("Invalid cefr value.")

    @staticmethod
    def __load_words_data() -> Dict[str, int]:
        """
        Loads the words data from the database.
        """
        path = os.path.join(os.path.dirname(__file__), '../data/cefr_levels.json')
        with open(path, 'r+') as f:
            return json.load(f)

    def validate(self, data: List[str]) -> (List[str], int):
        """
        Validates the value.

        :param data: List of words to validate.
        :return: True if the value is valid, False otherwise.
        """

        def eligible(phrase: str) -> bool:
            value = self.__get_phrase_cefr(phrase)
            if value == self.__LEVELS__[self.__UNKNOWN_LEVEL]:
                return not self.__filter_unknowns

            if value <= self.__min_cefr:
                return False
            if value > self.__max_cefr:
                return False
            return True

        eligible_items = [phrase for phrase in data if eligible(phrase)]
        return eligible_items, len(data) - len(eligible_items)

    def __get_phrase_cefr(self, phrase: str) -> int:
        return self.__words_data[phrase] if phrase in self.__words_data else self.__LEVELS__[self.__UNKNOWN_LEVEL]
