import logging
from typing import List

from game.Tempus.Classes.Character import Character, Attribute
from game.Tempus.utils.skillcheck import skillcheck


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
        result = skillcheck(party, path.attribute, path.difficulty) - 1
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

