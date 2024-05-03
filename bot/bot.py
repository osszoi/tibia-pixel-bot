import threading
import time

from bot.healer.healer import Healer


class Bot:
    @classmethod
    def init(cls):
        print("Initializing bot...")

        thread = threading.Thread(target=cls.run)
        thread.daemon = True
        thread.start()

    @classmethod
    def run(cls):
        while True:
            Healer.checkVitals()

            time.sleep(1)
