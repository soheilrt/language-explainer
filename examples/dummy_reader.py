import os

from composer.definition import DefinitionComposer
from definers.free_dictionary_api import FreeDictionaryDefiner
from middlewares.cefr import CEFRLimiter
from middlewares.char import CharLengthValidator
from middlewares.meaningful_words import MeaningfulWords
from middlewares.numbers import Number
from models.reader import Reader
from readers.pdfminer_reader import PDFMinerReader
from tokenizers.mwe_tokenize import MWETokenizer
from writers.json_writer import JsonFileWriter


class DummyReader(Reader):
    def read(self) -> str:
        return """central heating.
        I am trying to confirm if a matrix has a given cell/index in it. (In matrix [[A, B, C], [D, E, F]] does cell/index [0, 2] exist? Yes at C).
                """


def main():
    tokenizer = MWETokenizer()
    definer = FreeDictionaryDefiner()
    middlewares = [
        Number(),
        CharLengthValidator(min_length=3),
        MeaningfulWords(),
        CEFRLimiter(min_cefr=CEFRLimiter.LEVELS.C1)
    ]

    # reader = DummyReader()
    reader = PDFMinerReader(file_path=os.path.join(os.path.dirname(__file__), '../data/atomic-habits.pdf'))
    writer = JsonFileWriter(file_name="dummy_reader.json", indent=4)

    composer = DefinitionComposer(tokenizer=tokenizer, middlewares=middlewares, definer=definer)
    composer.compose_write(reader, writer)


main()
