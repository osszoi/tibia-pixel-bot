import math
import time


def pretty_print_time(milliseconds):
    if milliseconds >= 1000:
        # Convert to seconds if the milliseconds are 1000 or more
        seconds = milliseconds / 1000.0
        return f"{seconds:.2f} s"
    elif milliseconds < 0.001:
        # Convert to microseconds if less than 1 millisecond
        microseconds = milliseconds * 1000
        return f"{microseconds:.2f} us"
    else:
        # Print in milliseconds if it is between 1 ms and 1000 ms
        return f"{milliseconds:.2f} ms"


class Analytics:
    metrics = {}

    ongoing = {}

    @classmethod
    def timeStart(cls, name):
        cls.ongoing[name] = time.time()

    @classmethod
    def timeEnd(cls, name):
        if cls.ongoing[name] != None:
            t = (time.time() - cls.ongoing[name]) / 1000

            cls.metrics[name] = pretty_print_time(t)

            cls.ongoing[name] = None

            return pretty_print_time(t)
