from typing import Dict, List
import csv

from models.word import WordDefinition
from models.writer import Writer
from utils import url


class CSVWriter(Writer):
    __field_names = [
        'word',
        'phonetics',
        'phonetic audios',
        'part of speeches',
        'definitions',
        'examples',
        'synonyms',
        'antonyms',
        'translations',
    ]

    def __init__(self, file_name: str, write_header: bool = False):
        super().__init__()
        self.__file_name = file_name
        self.__write_header = write_header

    def write(self, data: Dict[str, List[WordDefinition]]):
        print("writing to csv, total {} words...".format(len(data)))

        with open(self.__file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.__field_names)

            if self.__write_header:
                writer.writeheader()

            word: str
            for word in data.keys():
                definition: WordDefinition = data[word][0] if len(data[word]) > 0 else []
                if not definition:
                    continue

                writer.writerow({
                    'word': word,
                    'phonetics': ' |-|-| '.join(
                        phonetic.phonetic for phonetic in definition.phonetics
                    ),
                    'phonetic audios': ' |-|-| '.join(
                        url.normalize(phonetic.audio) for phonetic in definition.phonetics
                    ),
                    'part of speeches': ' |-|-| '.join(
                        meaning.parOfSpeech for meaning in definition.meanings if meaning.parOfSpeech
                    ),
                    'definitions': ' |-|-| '.join(
                        ' ### '.join(str(d.definition) for d in meaning.definitions)
                        for meaning in definition.meanings if meaning.definitions
                    ),
                    'examples': ' |-|-| '.join(
                        ' ### '.join(d.example for d in meaning.definitions)
                        for meaning in definition.meanings if any(d.example for d in meaning.definitions)

                    ),
                    'synonyms': ' |-|-| '.join(
                        ' ### '.join(', '.join(d.synonyms) for d in meaning.definitions if d.synonyms)
                        for meaning in definition.meanings if any(d.synonyms for d in meaning.definitions)
                    ),
                    'antonyms': ' |-|-| '.join(
                        ' ### '.join(', '.join(d.antonyms) for d in meaning.definitions if d.antonyms)
                        for meaning in definition.meanings if any(d.antonyms for d in meaning.definitions)
                    ),
                    'translations': ' |-|-| '.join(
                        "{}: {} ### ".format(translation.partOfSpeech, translation.translation)
                        for translation in definition.translations if translation.translation
                    )
                })
