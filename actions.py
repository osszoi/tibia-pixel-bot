from keyboard import press, pressIfTarget
from utils import hasTarget, isLifeBelow, isManaBelow

battle = {
  "trigger": lambda: hasTarget(),
  "action": lambda keys=["F2", "F3", "F1"]: pressIfTarget(keys)
}

mana = {
  "trigger": lambda p=60: isManaBelow(p),
  "action": lambda keys="F9": press(keys)
}

heal = {
  "trigger": lambda p=95: isLifeBelow(p),
  "action": lambda keys="F10": press(keys)
}

lifePot = {
  "trigger": lambda p=40: isLifeBelow(p),
  "action": lambda keys="F11": press(keys)
}

actions = [lifePot, heal, mana, battle]
