import re
from typing import List

from models.middleware import Middleware


class Number(Middleware):
    def validate(self, data: List[str]) -> (List[str], int):
        """
        validate data and exclude tokens that contain numbers with regex

        :param data: The data to validate.
        :return: The validated data and the number of errors.
        """
        regex: re.Pattern = re.compile(r'\d')

        result = [token for token in data if not regex.match(token)]

        return result, len(data) - len(result)
