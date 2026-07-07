import logging
import random

from game.Tempus.Classes.Attribute import Attribute


def skillcheck(tries: int, difficulty: int = 4):
    success = 0
    tries += 1
    logging.debug(tries)
    while tries > 0:
        throw = random.randint(1, 10)
        if throw == 1:
            success -= 1
        elif throw == 10:
            success += 2
        elif throw >= difficulty:
            success += 1
        msg = str(throw) + " | " + str(difficulty)
        logging.debug(msg)
        tries -= 1
    return success


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(skillcheck(4, 10))
