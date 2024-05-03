from game.game import Game
from keyboard import KEYS, press


class Healer:

    @classmethod
    def checkVitals(cls):
        if Game.mana <= Game.maxMana * 0.8:
            press("F9")
