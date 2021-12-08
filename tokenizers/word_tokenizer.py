from typing import List
from nltk import word_tokenize

from models.tokenizer import Tokenizer


class WordTokenizer(Tokenizer):
    def tokenize(self, text) -> List[str]:
        return word_tokenize(text)
