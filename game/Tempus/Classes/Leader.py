from game.Tempus.Classes.Ability import Ability
from game.Tempus.Classes.Character import Character
from game.Tempus.Classes.HeathState import HealthState


class Leader(Character):
    def __init__(self, skill: Ability | None = None, hs: HealthState = HealthState.Full, **attributes: int):
        super().__init__(hs, **attributes)
        self.skill = skill
