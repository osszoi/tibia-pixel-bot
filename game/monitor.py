import threading
import time
from typing import List

from PIL import Image

from game.game import Game
from game.monsters import Monster, Monsters
from metrics import Analytics
from screen.ocr import preprocess_image_for_ocr
from screen.screen import Screen, image_to_np, load_image_as_np, send_image_to_clipboard


class GameMonitor:
    initialized = False

    fullVitalsRegion = None
    vitalsRegion = None

    battleRegion = None
    battle: List[str] = []

    @classmethod
    def init(cls):
        print("Initializing game monitor...")

        thread = threading.Thread(target=cls.run)
        thread.daemon = True
        thread.start()

    @classmethod
    def initPositions(cls):
        # Initialize vitals
        xpImage = load_image_as_np("resources/xp.png")
        xpBoostImage = load_image_as_np("resources/xp-boost.png")

        xpPosX, xpPosY = Screen.find(xpImage)
        xpBoostPosX, xpBoostPosY = Screen.find(xpBoostImage)

        cls.fullVitalsRegion = (xpPosX, xpPosY - 40, xpBoostPosX - xpPosX, 40)

        vitalsRegionImage = preprocess_image_for_ocr(
            Screen.extract_region(cls.fullVitalsRegion)
        )

        # Find / to make it smaller
        slashImage = load_image_as_np("resources/slash.png")
        slashPosX, slashPosY = Screen.find(slashImage, image_to_np(vitalsRegionImage))

        vitalsNumberLengthInPixels = 42

        cls.vitalsRegion = (
            slashPosX - vitalsNumberLengthInPixels,
            slashPosY - 2,
            vitalsNumberLengthInPixels * 2 + 10,
            30,
        )

        # Initialize battle
        battleImage = load_image_as_np("resources/battle-list.png")
        battlePosX, battlePosY = Screen.find(battleImage)
        battleWidth = 120
        battleHeight = 550
        cls.battleRegion = (battlePosX, battlePosY + 12, battleWidth, battleHeight)

    @classmethod
    def readVitals(cls):
        Analytics.timeStart("monitor__readVitals")

        vitalsRegionImage = preprocess_image_for_ocr(
            Screen.extract_region(cls.fullVitalsRegion)
        )

        smallVitalsPartImage = Screen.extract_region_from(
            cls.vitalsRegion, vitalsRegionImage
        )

        vitals = Screen.extract_numbers_from_image(smallVitalsPartImage)

        [hp, mana] = vitals.split("\n")
        [currentHp, totalHp] = hp.split("/")
        [currentMana, totalMana] = mana.split("/")

        Game.hp = int(currentHp)
        Game.mana = int(currentMana)
        Game.maxHp = int(totalHp)
        Game.maxMana = int(totalMana)

        Analytics.timeEnd("monitor__readVitals")

    @classmethod
    def readBattle(cls):
        Analytics.timeStart("monitor__readBattle")
        battlePartImage = Screen.extract_region(cls.battleRegion)

        allBatle: str = Screen.extract_text_from_image(battlePartImage)

        cls.battle = allBatle.split("\n")

        print(cls.battle)

        Analytics.timeEnd("monitor__readBattle")

    @classmethod
    def run(cls):
        while True:
            if Screen.latest_screenshot is None:
                time.sleep(0.01)
                continue

            if Screen.latest_screenshot is not None and cls.vitalsRegion is None:
                cls.initPositions()

            cls.readVitals()
            cls.readBattle()

            cls.initialized = True
            time.sleep(0.01)
