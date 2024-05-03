# import math

# import pyautogui

# from coordinates import (BATTLE_X, BATTLE_Y_OFFSET, BATTLE_Y_START, LIFE_Y,
#                          MANA_Y, STATUS_BARS_PIXELS, STATUS_BARS_START)

# PIXEL_ERROR_TOLERANCE = 0.1

# def isWithinValue(actual, expected, tolerance=PIXEL_ERROR_TOLERANCE):
#   bottomLimit = expected - expected * tolerance
#   upperLimit = expected + expected * tolerance

#   if actual >= bottomLimit and actual <= upperLimit:
#     return True

#   return False

# def hasTarget():
#   ss = pyautogui.screenshot()
#   height = ss.height
#   width = ss.width

#   yStart = BATTLE_Y_START

#   while yStart < height:
#     pixelY = yStart
#     pixel_color = ss.getpixel((BATTLE_X, pixelY))

#     if pixel_color == (255, 0 ,0) or pixel_color == (255, 128, 128):
#       return True

#     yStart += BATTLE_Y_OFFSET

#   return False

# def isStatusBarBelow(percentage, y, ss=None):
#   if ss == None:
#     ss = pyautogui.screenshot()

#   if percentage > 1:
#     percentage /= 100

#   pixelToCheck = STATUS_BARS_START + math.floor(STATUS_BARS_PIXELS * percentage)

#   r, g, b = ss.getpixel((pixelToCheck, y))
#   er, eg, eb = (69, 82, 109)

#   if isWithinValue(r, er) and isWithinValue(g, eg) and isWithinValue(b, eb):
#     return True

#   return False

# def isManaBelow(percentage, ss=None):
#   # print(f"Checking for mana below {percentage}")
#   return isStatusBarBelow(percentage, MANA_Y, ss)

# def isLifeBelow(percentage, ss=None):
#   # print(f"Checking for life below {percentage}")
#   return isStatusBarBelow(percentage, LIFE_Y, ss)
