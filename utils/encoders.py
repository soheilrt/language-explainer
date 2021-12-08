from json import JSONEncoder

from models.word import WordDefinition


class WordDefinitionJsonEncoder(JSONEncoder):
    def default(self, o: WordDefinition):
        def to_dict(item: any):
            if isinstance(item, list):
                for index in range(len(item)):
                    item[index] = to_dict(item[index])
            elif isinstance(item, dict):
                for entry in item:
                    item[entry] = to_dict(item[entry])
            else:
                try:
                    return to_dict(item.__dict__)
                except:
                    pass

            return item

        return to_dict(o.__dict__)
