from typing import List

from models.middleware import Middleware
import enchant


class MeaningfulWords(Middleware):
    def __init__(self, language: str = "en_US"):
        self.validator = enchant.Dict(language)

    def validate(self, data: List[str]) -> (List[str], int):
        """
        Validates the data.
        :param data: The data to validate.
        :return: The validated data and the number of errors.
        """

        meaningful_words = list(word for word in data if self.__is_eligible(word))
        return meaningful_words, len(data) - len(meaningful_words)

    def __is_eligible(self, phrase) -> bool:
        #  This is because we don't want to check phrases with more than one word since validator doesn't support it.
        if len(phrase.split(' ')) > 1:
            return True

        # This is because we don't want to have especial characters in our results since validator consider
        # special characters as meaningful word.
        if len(phrase) == 1 and phrase in '.!?,;:-_@#$%^&*()+={}[]|\\"\'<>/`~':
            return False

        return self.validator.check(word=phrase)
