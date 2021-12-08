from dataclasses import dataclass
from typing import List


@dataclass
class WordPhonetic:
    word: str
    language: str
    phonetic: str
    audio: str


@dataclass
class WordMeaningDefinition:
    definition: str
    example: str
    synonyms: List[str]
    antonyms: List[str]


@dataclass
class WordMeaning:
    parOfSpeech: str
    definitions: List[WordMeaningDefinition]


@dataclass
class WordTranslation:
    partOfSpeech: str
    word: str
    language: str
    translation: str


@dataclass
class WordDefinition:
    source: str
    word: str
    language: str
    origin: str
    phonetics: List[WordPhonetic]
    meanings: List[WordMeaning]
    translations: List[WordTranslation]

