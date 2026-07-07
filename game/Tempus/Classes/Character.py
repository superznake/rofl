from game.Tempus.Classes.Attribute import Attribute
from typing import Dict
from game.Tempus.Classes.HeathState import HealthState


class Character:
    def __init__(self, hs: HealthState = HealthState.Full, **attributes: int):
        self.hs = hs
        self.attributes: Dict[Attribute, int] = {}

        for attribute in Attribute:
            value = attributes.get(attribute.name, 0)
            self.attributes[attribute] = max(0, value)

    def get_attribute(self, attribute: Attribute) -> int:
        return self.attributes.get(attribute, 0)

    def __getitem__(self, attribute: Attribute) -> int:
        return self.get_attribute(attribute)
