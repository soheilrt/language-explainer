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
    ]

    def __init__(self, file_name: str):
        super().__init__()
        self.__file_name = file_name

    def write(self, data: Dict[str, List[WordDefinition]]):
        print("writing to csv, total {} words...".format(len(data)))

        with open(self.__file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.__field_names)

            word: str
            for word in data.keys():
                definition: WordDefinition = data[word][0] if len(data[word]) > 0 else []
                if not definition:
                    continue

                writer.writerow({
                    'word': word,
                    'phonetics': ' | '.join(
                        phonetic.phonetic for phonetic in definition.phonetics
                    ),
                    'phonetic audios': ' | '.join(
                        url.normalize(phonetic.audio) for phonetic in definition.phonetics
                    ),
                    'part of speeches': ' | '.join(
                        meaning.parOfSpeech for meaning in definition.meanings if meaning.parOfSpeech
                    ),
                    'definitions': ' \n '.join(
                        ', '.join(str(d.definition) for d in meaning.definitions) for meaning in definition.meanings
                    ),
                    'examples': ' | '.join(
                        ', '.join(d.example for d in meaning.definitions) for meaning in definition.meanings
                    ),
                    'synonyms': ' | '.join(
                        ', '.join(', '.join(d.synonyms) for d in meaning.definitions if d.synonyms)
                        for meaning in definition.meanings if any(d.synonyms for d in meaning.definitions)
                    ),
                    'antonyms': ' | '.join(
                        ', '.join(', '.join(d.antonyms) for d in meaning.definitions if d.antonyms)
                        for meaning in definition.meanings if any(d.antonyms for d in meaning.definitions)
                    ),
                    'translations': ' | '.join(
                        "{}: {}".format(translation.partOfSpeech, translation.translation)
                        for translation in definition.translations
                    )
                })
