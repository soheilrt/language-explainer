from typing import List

from models.middleware import Middleware


class Number(Middleware):
    def validate(self, data: List[str]) -> (List[str], int):
        """
        Validate the data and exclude only numbers data.

        :param data: The data to validate.
        :return: The validated data and the number of errors.
        """
        errors = 0
        validated_data = []
        for item in data:
            try:
                int(item)
                errors += 1
            except ValueError:
                validated_data.append(item)
        return validated_data, errors
