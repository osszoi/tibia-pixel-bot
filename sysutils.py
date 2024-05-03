import subprocess

import win32gui


def check_process_running(process_name):
    try:
        output = subprocess.check_output(["tasklist"], text=True)
        return process_name in output
    except subprocess.CalledProcessError:
        return False


def find_window(title):
    try:
        return win32gui.FindWindow(None, title)
    except win32gui.error:
        return None


def find_window_contains_title(title):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None
