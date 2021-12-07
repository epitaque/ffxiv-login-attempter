import pyautogui
import time
import random

while True:
    pyautogui.press('space')
    time.sleep(5 + random.randrange(15))