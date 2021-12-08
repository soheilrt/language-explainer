from typing import List, Dict, Union

import requests
import json

from models.definer import Definer, NotFoundException
from models.word import WordDefinition, WordPhonetic, WordMeaning, WordMeaningDefinition


class FreeDictionaryDefiner(Definer):
    __DEFINER_KEY = 'free_dictionary'
    __API_BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"
    __MEANING_DEFINITION_TYPE = Dict[str, Union[str, List[str]]]
    __MEANING_LIST_TYPE = List[Dict[str, Union[str, List[__MEANING_DEFINITION_TYPE]]]]
    __PHONETICS_TYPE = List[Dict[str, str]]

    def __init__(self):
        super().__init__()

    def define(self, word) -> List[WordDefinition]:
        response = requests.get(self.__API_BASE_URL.format(word))

        if response.status_code == 404:
            raise NotFoundException(f'definition of Word {word} not found')

        if response.status_code != 200:
            raise Exception(json.loads(response.text).get('title', 'Unknown Exception, {}'.format(response.text)))

        return self.__parse(word, response.text)

    def __parse(self, word, response_text: str) -> List[WordDefinition]:
        json_response = json.loads(response_text)
        return [self.__parse_single_entry(word, entry) for entry in json_response]

    def __parse_single_entry(self, word, entry: dict) -> WordDefinition:

        return WordDefinition(
            source=self.__DEFINER_KEY,
            word=word,
            language='en',
            origin=entry.get('origin', ''),
            phonetics=self.__parse_phonetics(word, phonetics=entry.get('phonetics', [])),
            meanings=self.__parse_meanings(meanings=entry.get('meanings', [])),
            translations=[]
        )

    @staticmethod
    def __parse_phonetics(word: str, phonetics: __PHONETICS_TYPE) -> List[WordPhonetic]:
        return [
            WordPhonetic(
                language='en',
                word=word,
                phonetic=item.get('text'),
                audio=item.get('audio'),
            )
            for item in phonetics
            if 'audio' in item and 'text' in item
        ]

    def __parse_meanings(self, meanings: __MEANING_LIST_TYPE) -> List[WordMeaning]:
        word_meanings = list()
        for meaning in meanings:
            word_meaning = WordMeaning(
                parOfSpeech=meaning.get('partOfSpeech', None),
                definitions=self.__parse_word_meaning_definitions(meaning.get('definitions', [])),
            )

            word_meanings.append(word_meaning)

        return word_meanings

    @staticmethod
    def __parse_word_meaning_definitions(meaning_definitions: List[__MEANING_DEFINITION_TYPE]) \
            -> List[WordMeaningDefinition]:
        return [
            WordMeaningDefinition(
                definition=definition.get('definition', ''),
                example=definition.get('example', ''),
                synonyms=definition.get('synonyms', []),
                antonyms=definition.get('antonyms', []),
            )
            for definition in meaning_definitions
        ]
