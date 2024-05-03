import time

import win32api
import win32con

from sysutils import find_window_contains_title

KEYS = {
    # Alphabet
    "A": 0x41,
    "B": 0x42,
    "C": 0x43,
    "D": 0x44,
    "E": 0x45,
    "F": 0x46,
    "G": 0x47,
    "H": 0x48,
    "I": 0x49,
    "J": 0x4A,
    "K": 0x4B,
    "L": 0x4C,
    "M": 0x4D,
    "N": 0x4E,
    "O": 0x4F,
    "P": 0x50,
    "Q": 0x51,
    "R": 0x52,
    "S": 0x53,
    "T": 0x54,
    "U": 0x55,
    "V": 0x56,
    "W": 0x57,
    "X": 0x58,
    "Y": 0x59,
    "Z": 0x5A,
    # Numbers
    "Num0": 0x30,
    "Num1": 0x31,
    "Num2": 0x32,
    "Num3": 0x33,
    "Num4": 0x34,
    "Num5": 0x35,
    "Num6": 0x36,
    "Num7": 0x37,
    "Num8": 0x38,
    "Num9": 0x39,
    # Numpad numbers
    "NumPad0": 0x60,
    "NumPad1": 0x61,
    "NumPad2": 0x62,
    "NumPad3": 0x63,
    "NumPad4": 0x64,
    "NumPad5": 0x65,
    "NumPad6": 0x66,
    "NumPad7": 0x67,
    "NumPad8": 0x68,
    "NumPad9": 0x69,
    # Special characters
    "Spacebar": 0x20,
    "Enter": 0x0D,
    "Tab": 0x09,
    "Backspace": 0x08,
    "Esc": 0x1B,
    # Function keys
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "F12": 0x7B,
    # Control keys
    "Shift": 0x10,
    "Ctrl": 0x11,
    "Alt": 0x12,
    "LeftShift": 0xA0,
    "RightShift": 0xA1,
    "LeftControl": 0xA2,
    "RightControl": 0xA3,
    "LeftMenu": 0xA4,  # Left Alt
    "RightMenu": 0xA5,  # Right Alt
}


def send_virtual_key_to_background_window(vk, hwnd):
    """
    Send a virtual key to a background window.

    Args:
    vk: Virtual key code (integer).
    hwnd: Handle to the window (integer).
    """
    # Sending the key down message
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk, 0)

    # Optional: add a slight delay
    time.sleep(0.1)  # 100 milliseconds

    # Sending the key up message
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk, 0)


def press(keys):
    if isinstance(keys, str):
        pressBackground(keys)
    elif isinstance(keys, list):
        for key in keys:
            pressBackground(key)


def pressBackground(key):
    handle = find_window_contains_title("Tibia - ")

    send_virtual_key_to_background_window(KEYS[key], handle)
