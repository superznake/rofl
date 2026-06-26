from enum import Enum
from typing import Dict


class Attribute(Enum):
    Dex = 1
    Pow = 2
    Int = 3


class Character:
    def __init__(self, skill=None, **attributes: int):
        self.attributes: Dict[Attribute, int] = {}

        for attribute in Attribute:
            value = attributes.get(attribute.name, 0)
            self.attributes[attribute] = max(0, value)

    def get_attribute(self, attribute: Attribute) -> int:
        return self.attributes.get(attribute, 0)

    def __getitem__(self, attribute: Attribute) -> int:
        """Чтобы можно было писать char[Skill.Dex]"""
        return self.get_attribute(attribute)
