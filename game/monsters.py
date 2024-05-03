from enum import Enum
from typing import List


class Monster(Enum):
    TrainingMonk = {"name": "Training Monk"}


class Monsters:
    allMonsters: List[Monster] = [Monster.TrainingMonk]
