import pyautogui
from pywinauto.application import Application

from utils import hasTarget


def press(keys, useAsync=False):
  if isinstance(keys, str):
    if useAsync:
      pressAsync(keys)
    else:
      pyautogui.press(keys)
  elif isinstance(keys, list):
    for key in keys:
      if useAsync:
        pressAsync(key)
      else:
        pyautogui.press(key)

def pressIfTarget(keys):
  if hasTarget():
    press(keys)

def pressAsync(keys):
  windowTitle = "Tibia - Arkangelitox"
  app = Application().connect(title=windowTitle, timeout=1)
  window = app.window(title=windowTitle)

  # window.set_focus()

  for key in keys:
    window.type_keys(f"{{{key}}}", with_spaces=True)
