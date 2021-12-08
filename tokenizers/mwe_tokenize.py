import json
import os.path
from typing import List

from models import tokenizer
from nltk.tokenize import MWETokenizer as NltkMWETokenizer

from tokenizers.word_tokenizer import WordTokenizer


class MWETokenizer(tokenizer.Tokenizer):
    def __init__(self):
        self.__word_tokenizer = WordTokenizer()
        self.__mwe_tokenizer = self.__init_mwe_tokenizer()

    def tokenize(self, text: str) -> List[str]:
        tokenized = self.__mwe_tokenizer.tokenize(self.__word_tokenizer.tokenize(text))
        return [token.replace('_', ' ') for token in tokenized]

    def __init_mwe_tokenizer(self) -> NltkMWETokenizer:
        mwes = list()
        with open(os.path.join(os.path.dirname(__file__), '../data/cefr_levels.json'), 'r') as f:
            tokens = json.load(f)
            for token in tokens.keys():
                expression = token.split(' ')
                if len(expression) > 1:
                    expression = [word.replace('(', '').replace(')', '') for word in expression]
                    mwes.append(tuple(expression))

        return NltkMWETokenizer(mwes=mwes)
