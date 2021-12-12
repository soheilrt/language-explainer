import json
from typing import List, Dict

from models.word import WordDefinition
from models.writer import Writer
from utils.encoders import WordDefinitionJsonEncoder


class JsonFileWriter(Writer):
    def __init__(self, file_name: str, indent=4, sort_keys=True, ensure_ascii=False):
        self.file = open(file_name, 'w')
        self.indent = indent
        self.sort_keys = sort_keys
        self.ensure_ascii = ensure_ascii

    def write(self, data: Dict[str, List[WordDefinition]]):
        json.dump(
            data,
            self.file,
            cls=WordDefinitionJsonEncoder,
            indent=self.indent,
            sort_keys=self.sort_keys,
            ensure_ascii=self.ensure_ascii
        )
