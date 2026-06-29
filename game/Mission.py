import logging
import random
from typing import List

from game.Character import Character, Attribute


class Path:
    def __init__(self, difficulty: int, attribute: Attribute, extra_reward: int | None):
        self.difficulty = difficulty
        self.attribute = attribute
        self.extra_reward = extra_reward


class Mission:
    def __init__(self, rewards: int, pathA: Path, pathB: Path):
        self.pathA = pathA
        self.pathB = pathB
        self.rewards = rewards

    def tryPath(self, path: str, party: List[Character]):
        if path.upper() == "A":
            path = self.pathA
        elif path.upper() == "B":
            path = self.pathB
        else:
            logging.warning("Wrong path data")
            return -1
        result = SkillCheck(party, path.attribute, path.difficulty) - 1
        if result < 0:
            logging.info("mission failed")
            return 0
        elif result == 0:
            logging.info("mission succeeded")
            # TODO: apply_rewards(rewards)
            return 1
        else:
            logging.info("mission extra succeeded")
            if path.extra_reward:
                garant = 0  # TODO: garant system for extra reward
                gathered = False
                while (result > 0) and not gathered:
                    result -= 1
                    res = 0  # TODO: magic formula for extra reward
                    if res:
                        gathered = True
                    else:
                        garant += 1
                if gathered:
                    logging.info("extra reward gathered")
                    # TODO: apply_rewards(path.extra_rewards)
                else:
                    logging.info("extra reward not gathered")
                return 2
            return 1


def SkillCheck(chars: List[Character], attribute: Attribute, difficulty: int = 4):
    logging.info(attribute)
    success = 0
    tries = 0
    for char in chars:
        tries += char[attribute]
    logging.info(tries)
    for i in range(tries):
        throw = random.randint(1, 10)
        if throw == 1:
            success -= 1
        elif throw == 10:
            success += 2
        elif throw >= difficulty:
            success += 1
        msg = str(throw) + " | " + str(difficulty)
        logging.info(msg)
    return success
