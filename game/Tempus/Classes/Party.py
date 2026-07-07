import logging
from typing import List

from game.Tempus.Classes.Character import Character
from game.Tempus.Classes.Leader import Leader


class Party:
    def __init__(self, leader: Leader, chars: List[Character]):
        self.leader = leader
        self.chars = chars

    def get_members(self):
        result = [self.leader]
        for char in self.chars:
            result.append(char)
        return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    charA = Character(Pow=4)
    charB = Character(Pow=2, Int=2)
    charC = Leader(None, Pow=3, Int=1)
    party = Party(charC, [charA, charB])

    print(party.get_members())
