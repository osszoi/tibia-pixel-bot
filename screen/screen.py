import ctypes
import threading
import time
from ctypes import wintypes

import cv2
import numpy as np
import win32clipboard
import win32con
import win32gui
import win32ui
from PIL import Image

from metrics import Analytics
from screen.ocr import (
    extract_numbers_from_image,
    extract_text_from_image,
    preprocess_image_for_ocr,
)
from sysutils import find_window_contains_title


def send_image_to_clipboard(image):
    """Save a PIL image to the clipboard on Windows"""
    output = "temp_clipboard.bmp"
    image.save(output, "BMP")
    data = open(output, "rb").read()
    win32clipboard.OpenClipboard()  # Open the clipboard
    win32clipboard.EmptyClipboard()  # Clear the clipboard
    win32clipboard.SetClipboardData(
        win32clipboard.CF_DIB, data[14:]
    )  # CF_DIB is used for a Device Independent Bitmap
    win32clipboard.CloseClipboard()


def image_to_np(image):
    r = np.array(image.convert("RGB"))

    return r[:, :, ::-1]


def load_image_as_np(path):
    image = Image.open(path)
    r = np.array(image.convert("RGB"))

    return r[:, :, ::-1]


class Screen:
    initialized = False
    t = None
    latest_screenshot = None
    latest_screenshot_np = None
    latest_preprocessed_screenshot = None
    latest_preprocessed_screenshot_np = None

    @classmethod
    def init(cls):
        print("Initializing screen capturer...")
        thread = threading.Thread(target=cls.run)
        thread.daemon = True
        thread.start()

    @classmethod
    def capture(cls):
        Analytics.timeStart("screen__capture")

        hWnd = find_window_contains_title("Tibia - ")

        if win32gui.IsIconic(hWnd):
            win32gui.ShowWindow(hWnd, win32con.SW_RESTORE)

        rect = win32gui.GetWindowRect(hWnd)
        if not rect:
            return None

        width = rect[2] - rect[0]
        height = rect[3] - rect[1]

        hwndDC = win32gui.GetWindowDC(hWnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitmap = win32ui.CreateBitmap()
        saveBitmap.CreateCompatibleBitmap(mfcDC, width, height)

        saveDC.SelectObject(saveBitmap)

        result = ctypes.windll.user32.PrintWindow(hWnd, saveDC.GetSafeHdc(), 1)

        bmpinfo = saveBitmap.GetInfo()
        bmpstr = saveBitmap.GetBitmapBits(True)

        cls.latest_screenshot = Image.frombuffer(
            "RGB",
            (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
            bmpstr,
            "raw",
            "BGRX",
            0,
            1,
        )

        cls.latest_screenshot_np = np.array(cls.latest_screenshot)
        cls.latest_screenshot_np = cls.latest_screenshot_np[:, :, ::-1]

        win32gui.DeleteObject(saveBitmap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hWnd, hwndDC)
        Analytics.timeEnd("screen__capture")

    @classmethod
    def run(cls):
        while True:
            cls.capture()

            cls.latest_preprocessed_screenshot = preprocess_image_for_ocr(
                cls.latest_screenshot
            )

            cls.initialized = True
            time.sleep(1 / 20)

    @classmethod
    def extract_numbers_from_image(cls, image):
        return extract_numbers_from_image(image)

    @classmethod
    def extract_text_from_image(cls, image):
        return extract_text_from_image(image)

    @classmethod
    def find(cls, t, f=None):
        if f is None:
            f = cls.latest_screenshot_np

        ss_gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        t_gray = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(ss_gray, t_gray, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.8:
            return max_loc
        else:
            return None

    @classmethod
    def find_from_file(cls, path):
        t = cv2.imread(path)

        if t is None:
            raise FileNotFoundError(f"File {path} not found")

        return cls.find(t)

    @classmethod
    def extract_region(cls, region):
        return cls.extract_region_from(region, cls.latest_screenshot)

    @classmethod
    def extract_region_from(cls, region, src):
        if src is not None:
            x, y, width, height = region

            box = (x, y, x + width, y + height)

            return src.crop(box)

        return None
