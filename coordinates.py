import math

import pyautogui


def toAnyScreenWidth(n):
  return SCREEN_WIDTH - (BASE_SCREEN_WIDTH - n)

BASE_SCREEN_WIDTH = 2560
BASE_SCREEN_HEIGHT = 1440

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Status bars (life, mana)
BASE_STATUS_BARS_START = 2408
BASE_STATUS_BARS_END = 2497

# Actual coords on any screen
STATUS_BARS_START = toAnyScreenWidth(BASE_STATUS_BARS_START)
STATUS_BARS_END = toAnyScreenWidth(BASE_STATUS_BARS_END)
STATUS_BARS_PIXELS = STATUS_BARS_END - STATUS_BARS_START

LIFE_Y = 147
MANA_Y = 160

# Battle target
BASE_BATTLE_X = 2220 # 2nd panel from right to left
BATTLE_Y_START = 86 # first monster, having "configure" dropdown opened
BATTLE_Y_OFFSET = 22

# Actual coords on any screen
BATTLE_X = toAnyScreenWidth(BASE_BATTLE_X)
