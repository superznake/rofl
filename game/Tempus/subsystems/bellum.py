# game engine
import logging
import random
from typing import Dict, List

from game.Tempus.Classes.Attribute import Attribute
from game.Tempus.Classes.Character import Character
from game.Tempus.Classes.Leader import Leader
from game.Tempus.Classes.Party import Party
from game.Tempus.Classes.HeathState import HealthState
from game.Tempus.Classes.BattleState import BattleState
from game.Tempus.utils.skillcheck import skillcheck


def fight(attackers: Party, defenders: Party, **mods):
    # prep
    bi_A = get_battle_info(attackers, True)
    bi_D = get_battle_info(defenders, True)
    # initiative
    turn_order = create_init_list(bi_A, bi_D)
    # battle
    battle_ended = False
    while not battle_ended:
        for char in turn_order:
            attacker = char["char"]
            defence = choose_target()
            defender = defence["char"]
            attack = skillcheck(attacker[Attribute.Pow], 6)
            if attack > 0:
                damage = skillcheck(attacker[Attribute.Pow]+attack, 6) - defender[Attribute.Pow]
                if damage > 0:
                    defence["health"] -= damage
                    if defence["health"] <= 0:
                        defence["states"].append(BattleState.Dead)
            elif char["health"] <= (HealthState.Full.value/2):
                if skillcheck(attacker[Attribute.Soc]+1*char["is_leader"], 6) > 0:
                    diff = 0
                    body = False
                    for c in turn_order:
                        if (BattleState.Dead in c["states"] and c["char"] != attacker
                                and c["is_attack"] == char["is_attack"]):
                            if skillcheck(c["char"][Attribute.Soc], 5) > 0:
                                body = c
                                take = skillcheck(attacker[Attribute.Pow], 7)
                                if take < 0:
                                    diff = 1
                                    body = False
                                elif take == 0:
                                    diff = 1
                    if skillcheck(attacker[Attribute.Pow], 6+diff) > 0:
                        turn_order.pop(attacker)
                        if body:
                            turn_order.pop(body)
            only_one_team = True
            for c in turn_order:
                if c["char"] != attacker and (c["is_attack"] != char["is_attack"] and not BattleState.Dead in c["states"]):
                    only_one_team = False
            if only_one_team:
                battle_ended = True
    # get and apply result
    ...


def get_battle_info(party: Party, is_attack: bool = False):
    battle_data = []
    leader = party.leader
    leader_initiative = ((leader[Attribute.Pow] + leader[Attribute.Int] + random.randint(1, 10)) * 10 +
                         (int(is_attack) * 5))
    battle_data.append({
        "char": leader,
        "health": leader.hs.value,
        "initiative": leader_initiative,
        "is_attack": is_attack,
        "states": [],
        "is_leader": True
    })
    for char in party.chars:
        initiative = ((char[Attribute.Pow] + char[Attribute.Int] + random.randint(1, 10)) * 10 +
                      (int(is_attack) * 5))
        battle_data.append({
            "char": char,
            "health": char.hs.value,
            "initiative": initiative,
            "is_attack": is_attack,
            "states": [],
            "is_leader": False
        })
    return battle_data


def create_init_list(partyA: List, partyB: List):
    order = partyA + partyB
    return sorted(order, key=lambda x: x["initiative"], reverse=True)


def choose_target():
    ...
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    charA = Character(Pow=4)
    charB = Character(Pow=2, Int=2)
    charC = Leader(None, Pow=3, Int=1)
    pA = Party(charC, [charA, charB])
    print(get_battle_info(pA))


"""
Battle info: 
health
initiative
is_attack
states
is_leader
"""


""" ...
chars: List[Character]
for char in chars:
    tries += char[attribute]
"""