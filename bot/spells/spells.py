from enum import Enum

from screen.screen import Screen


class Spell(Enum):
    ExoriGran = "knight/exorigran"


class Spells:
    allSpells = [Spell.ExoriGran]

    @classmethod
    def isOnCooldown(cls, spell: Spell) -> bool:
        return (
            False
            if Screen.find_from_file(f"resources/spells/{spell.value}.png")
            else True
        )
