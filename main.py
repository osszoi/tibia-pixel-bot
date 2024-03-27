import time

from actions import actions

while True:
    for action in actions:
      if action["trigger"]():
          action["action"]()

    time.sleep(0.5)
