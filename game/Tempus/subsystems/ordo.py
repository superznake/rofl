# fair random

import logging
from enum import Enum
from typing import List, Dict

from game.Tempus.Classes.Character import Character, Attribute


class Clan(Enum):
    Bruha = 1
    Gangrel = 2
    Malkavian = 3
    Nosferatu = 4
    Toreador = 5
    Tremer = 6
    Ventru = 7


def generateRoster(clan: Clan, style: int, base_points: int = 40):
    points = base_points
    roster = getLeaders(clan, style)
    points -= calc_points(roster)
    logging.info(f"points point after leaders: {points}")
    buf = generateSpecialists(clan)
    logging.debug(f"roster b Specialists: {roster}")
    for char in buf:
        roster.append(char)
    logging.debug(f"roster a Specialists: {roster}")
    points = base_points
    points -= calc_points(roster)
    logging.info(f"points point after specialists: {points}")
    roster.append(generateVersatile(clan))
    logging.debug(f"roster a Versatile: {roster}")
    points = base_points
    points -= calc_points(roster)
    logging.info(f"points point after versatile: {points}")
    for char in generateOthers(points, clan):
        roster.append(char)
    return roster


def getLeaders(clan, style):
    result: List[Character] = []
    # TODO
    if style == 0:
        result.append(Character(Dex=3))
    elif style == 1:
        result.append(Character(Dex=1, Pow=1))
    result.append(Character(Int=2, Dex=1, Pow=1))
    return result


def generateSpecialists(clan):
    result: List[Character] = []
    for att in Attribute:
        result.append(Character(**{att.name: 5}))
    logging.debug(f"Specialists: {result}")
    return result


def generateVersatile(clan):
    atts: Dict[str, int] = {}
    for att in Attribute:
        atts[att.name] = 2

    result = Character(**atts)
    logging.debug(f"Versatile: {result}")
    return result


def generateOthers(points, clan):
    result: List[Character] = []

    return result


def calc_points(chars: List[Character]):
    result = 0
    for char in chars:
        result += sum(char.attributes.values())
        logging.debug(f"char: {char}\npoints : {result}")
    logging.info(f"point calculated: {result}")
    return result
