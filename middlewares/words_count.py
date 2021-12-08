from typing import List, Optional

from models.middleware import Middleware


class WordCountLimiter(Middleware):
    def __init__(self, min_repeats: Optional[int] = None, max_repeats: Optional[int] = None):
        self.__validate_repeats(min_repeats, max_repeats)
        self.min_repeats = min_repeats
        self.max_repeats = max_repeats

    def __validate_repeats(self, min_repeats: int, max_repeats: int):
        if min_repeats is not None and min_repeats < 0:
            raise ValueError('Min repeats count is less than 0')
        if max_repeats is not None and max_repeats < 0:
            raise ValueError('Max repeats count is less than 0')
        if min_repeats is not None and max_repeats is not None and min_repeats < max_repeats:
            raise ValueError('Min repeats count is less than max repeats count')

    def validate(self, words: List[str]) -> (List[str], int):
        """
        :param words: List of words to check
        :return: List of words with limited count of repeats
        """

        words_dict = dict()
        for word in words:
            if word not in words_dict:
                words_dict[word] = 0
            words_dict[word] += 1

        eligible_words = list()
        for word in words_dict:
            if self.max_repeats is not None and self.min_repeats is not None:
                if not self.max_repeats > words_dict[word] >= self.min_repeats:
                    continue
            elif self.min_repeats is not None:
                if self.min_repeats >= words_dict[word]:
                    continue
            elif self.max_repeats is not None:
                if self.max_repeats < words_dict[word]:
                    continue

            eligible_words.append(word)

        return eligible_words, len(words) - len(words_dict)
