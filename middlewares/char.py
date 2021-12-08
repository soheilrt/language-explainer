from typing import List

from models.middleware import Middleware


class CharLengthValidator(Middleware):
    def __init__(self, min_length=0, max_length=100):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, data: List[str]) -> (List[str], int):
        def eligible(item: str) -> bool:
            return self.min_length <= len(item) <= self.max_length

        eligible_items = [item for item in data if eligible(item)]
        return eligible_items, len(data) - len(eligible_items)
