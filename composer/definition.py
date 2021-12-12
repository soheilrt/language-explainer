from typing import List, Dict, Set

from models.composer import Composer
from models.definer import Definer, NotFoundException
from models.reader import Reader
from models.tokenizer import Tokenizer
from models.middleware import Middleware
from models.word import WordDefinition
from models.writer import Writer


class DefinitionComposer(Composer):
    """
    Definition composer class
    """

    def __init__(self, tokenizer: Tokenizer, middlewares: List[Middleware], definer: Definer, verbose: bool = False):
        """
        Definition composer constructor
        :param tokenizer: tokenizes the input
        :param middlewares: validates tokenized input whether it is acceptable
        :param definer: defines validated input words
        """
        self.tokenizer: Tokenizer = tokenizer
        self.middlewares: List[Middleware] = middlewares
        self.definer: Definer = definer
        self.verbose: bool = verbose

    def compose(self, reader: Reader) -> Dict[str, List[WordDefinition]]:
        """
        Compose definition
        """
        tokenized = self.tokenizer.tokenize(reader.read())
        print("number of words that found: " + str(len(tokenized)))
        normalized = self.__normalize_data(tokenized)
        print("number of words after normalization: " + str(len(normalized)))

        for middleware in self.middlewares:
            normalized, excluded = middleware.validate(normalized)
            print("{} words excluded by {}".format(excluded, middleware.__class__.__name__))

        print("words remained: {}".format(len(normalized)))
        print('defining...')
        definitions = dict()
        for word in normalized:
            try:
                definitions[word] = self.definer.define(word)
                if self.verbose:
                    print("word `{}` defined".format(word))
            except NotFoundException:
                if self.verbose:
                    print("word `{}` not found".format(word))
        print("number of words defined: {} out of {}".format(len(definitions), len(normalized)))
        return definitions

    def compose_write(self, reader: Reader, writer: Writer) -> None:
        """
        Compose definition and write to file
        """
        writer.write(self.compose(reader))

    @staticmethod
    def __normalize_data(tokenized: List[str]) -> Set[str]:
        """
        Normalize data
        """
        return set(word.lower() for word in tokenized)
