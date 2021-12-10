from typing import List

from nltk import word_tokenize

from models.tokenizer import Tokenizer


class WordTokenizer(Tokenizer):
    __punctuations: str = '!"#$%&\'()*+,./:;<=>?@[\\]^_-`{|}~'

    def tokenize(self, text) -> List[str]:
        return word_tokenize(self.__translate_punctuations_to_space(text))

    def __translate_punctuations_to_space(self, text):
        return text.translate(str.maketrans(self.__punctuations, ' ' * len(self.__punctuations)))
