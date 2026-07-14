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
    bi_D = get_battle_info(defenders, False)
    # initiative
    turn_order = create_init_list(bi_A, bi_D)
    logging.debug("Turn order")
    # battle
    winner = None
    battle_ended = False
    rounds = 0
    while not battle_ended:
        rounds += 1
        logging.info(f"Round: №{rounds}")
        turns = 0
        if turn_order:
            for char in turn_order[:]:
                if char not in turn_order:
                    continue
                attacker = char["char"]
                if BattleState.Dead not in char["states"]:
                    turns += 1
                    logging.debug(f"Turn: №{turns}")
                    defence = choose_target(char, turn_order)
                    if defence:
                        defender = defence["char"]
                        logging.debug(f"Attacker: {char} | Defender: {defence}")
                        attack = skillcheck(attacker[Attribute.Pow], 6)
                        logging.debug(f"Attack: {attack}")
                        if attack > 0:
                            damage = skillcheck(attacker[Attribute.Pow] + attack, 6) - skillcheck(defender[Attribute.Pow], 6)
                            logging.debug(f"Damage: {damage}")
                            if damage > 0:
                                defence["health"] -= damage
                                if defence["health"] <= 0:
                                    defence["states"].append(BattleState.Dead)
                                    logging.debug(f"{defender} is dead")
                        elif char["health"] <= (HealthState.Full.value / 2):
                            if skillcheck(attacker[Attribute.Soc] + 1 * char["is_leader"], 6) > 0:
                                logging.debug("Decided to escape")
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
                                if skillcheck(attacker[Attribute.Pow], 6 + diff) > 0:
                                    turn_order.remove(char)
                                    logging.debug("Escaped")
                                    if body:
                                        turn_order.remove(body)
                    only_one_team = True
                    for z in turn_order:
                        #logging.info(f"Z: {z}")
                        if z["char"] != attacker:
                            #logging.info("Z is not char")
                            if z["is_attack"] != char["is_attack"]:
                                #logging.info("Z is not in char team")
                                if BattleState.Dead not in z["states"]:
                                    #logging.info("Z is not dead")
                                    only_one_team = False
                    if only_one_team:
                        battle_ended = True
                        winner = char["is_attack"]
                        logging.debug(f"Battle ended. Winner is attacker: {winner}")
    # get and apply result
    return winner


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


def choose_target(attacker, poss_targets):
    targets = [
        t for t in poss_targets
        if t is not attacker
        and BattleState.Dead not in t["states"]
        and (attacker["is_attack"] != t["is_attack"] or BattleState.Confused in attacker["states"])
    ]
    if not targets:
        result = None
    else:
        result = random.choice(targets)
    return result


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)

    charAa = Character(Pow=4)
    charBa = Character(Pow=2, Int=2)
    charCa = Leader(None, Pow=3, Int=1)
    pA = Party(charCa, [charAa, charBa])
    charAb = Character(Pow=4)
    charBb = Character(Pow=2, Int=2)
    charCb = Leader(None, Pow=3, Int=1)
    pB = Party(charCb, [charAb, charBb])
    # print(get_battle_info(pA))
    with open('stats.txt', 'w', encoding='utf-8') as f:
        for j in range(900):
            counter = 0
            for i in range(100):
                if fight(pA, pB):
                    counter += 1
            f.write(str(counter)+"\n")
    print("READY")

"""
Battle info: 
health
initiative
is_attack
states
is_leader
"""
