# Before running this script, run:
# pip install pyautogui opencv-python Pillow

import pyautogui
import time
from enum import Enum
import subprocess
import psutil

def is_ffxiv_running():
    processName = "ffxiv"
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

class State(Enum):
    FFXIV_NOT_OPENED=0
    MAIN_MENU=1
    CHARACTER_SELECTION_SCREEN=2
    CHARACTER_LOGIN_PROMPT_OR_ERROR=3
    WAITING_IN_QUEUE=4
    ERROR_2002=5
    UNKNOWN=6

ffxiv_executable = r'C:\Users\Brian\AppData\Local\XIVLauncher\XIVLauncher.exe'
sleep_time = 5

def detect_state():
    if not is_ffxiv_running():
        return State.FFXIV_NOT_OPENED
    elif try_detect("state_mainMenu.png"):
        return State.MAIN_MENU
    elif try_detect("state_inQueue.png"):
        return State.WAITING_IN_QUEUE
    elif try_detect("button_characterLoginPrompt.png"):
        return State.CHARACTER_LOGIN_PROMPT_OR_ERROR
    elif try_detect("state_characterSelectionScreen.png"):
        return State.CHARACTER_SELECTION_SCREEN
    elif try_detect("button_okay.png"):
        return State.ERROR_2002
    return State.UNKNOWN

def try_detect(image_url, confidence=0.7):
    try:
        location = pyautogui.locateOnScreen(image_url, confidence=confidence)
        if location == None:
            return False
        return True
    except pyautogui.ImageNotFoundException:
        return False

def try_locate_and_click_button(image_url, offsetX=0, offsetY=0, confidence=0.7):
    try:
        location = pyautogui.locateOnScreen(image_url, confidence=confidence)
        if location == None:
            return None

        center = pyautogui.center(location)
        offsetX = center[0] + offsetX
        offsetY = center[1] + offsetY
        pyautogui.moveTo(offsetX, offsetY)
        time.sleep(1)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(1)
        # move it back to avoid messing up state detection
        pyautogui.moveTo(5, 5)
        return True
    except pyautogui.ImageNotFoundException:
        return None

while True:
    current_state = detect_state()
    print(f"Current state: {current_state}.")
    action_success = None

    if current_state == State.FFXIV_NOT_OPENED:
        subprocess.Popen([ffxiv_executable])
        time.sleep(30)
        action_success = is_ffxiv_running()
    elif current_state == State.MAIN_MENU:
        action_success = try_locate_and_click_button("button_mainMenuStart.png")
    elif current_state == State.CHARACTER_SELECTION_SCREEN:
        action_success = try_locate_and_click_button("state_characterSelectionScreen.png", offsetX=0, offsetY=150)
    elif current_state == State.CHARACTER_LOGIN_PROMPT_OR_ERROR:
        action_success = try_locate_and_click_button("button_characterLoginPrompt.png")
    elif current_state == State.WAITING_IN_QUEUE:
        action_success = True
    elif current_state == State.ERROR_2002:
        action_success = try_locate_and_click_button("button_okay.png")
    else:
        print(f"I don't know what to do in state {current_state}.")

    if action_success != True:
        print(f"We did not successfully perform our action corresponding to this state.")

    time.sleep(sleep_time)

