# import time

# from actions import actions

# while True:
#     for action in actions:
#       if action["trigger"]():
#           action["action"]()

#     time.sleep(0.5)

import time

from PIL import Image

from bot.bot import Bot
from game.monitor import GameMonitor
from metrics import Analytics
from screen.screen import Screen, send_image_to_clipboard


def main():
    # Main loop
    Analytics.timeStart("init__screen")
    Screen.init()
    while not Screen.initialized:
        time.sleep(0.01)
        continue
    initScreenTime = Analytics.timeEnd("init__screen")
    print(f"Screen capture initialized ({initScreenTime})")

    Analytics.timeStart("init__gameMonitor")
    GameMonitor.init()
    while not GameMonitor.initialized:
        time.sleep(0.01)
        continue
    initGameMonitorTime = Analytics.timeEnd("init__gameMonitor")
    print(f"Game monitor initialized ({initGameMonitorTime})")

    Analytics.metrics.clear()

    Bot.init()

    while True:
        print(Analytics.metrics)

        time.sleep(1)


if __name__ == "__main__":
    main()
