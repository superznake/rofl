import logging

from game.Character import Character, Attribute
from game.Mission import SkillCheck, Path, Mission
from game.ordo import generateRoster, Clan

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    charA = Character(Dex=4)
    charB = Character(Dex=2, Pow=2)
    Party = [charA, charB]
#    print(SkillCheck(Party, Attribute.Dex))
#   print(SkillCheck(Party, Attribute.Pow))
#  print(SkillCheck(Party, Attribute.Int))

#    pathA = Path(6, Attribute.Dex, 2)
#    pathB = Path(5, Attribute.Int, 1)
#    mission = Mission(4, pathA, pathB)
#    print("preA")
#    print(mission.tryPath("A", Party))
#    print("preB")
#    print(mission.tryPath("B", Party))
#    print("...")

    print(generateRoster(Clan.Bruha, 0))
