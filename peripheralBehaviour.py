import keyboard
import pyautogui
import time
from pynput.mouse import Controller as MouseController

Mouse = MouseController()
defaultTimeToWait = 0.075

def onlyPressButton(button):
    Mouse.press(button)

def onlyReleaseButton(button):
    Mouse.release(button)

def clickButton(button, seconds = defaultTimeToWait):
    Mouse.press(button)
    time.sleep(seconds)
    Mouse.release(button)
    time.sleep(seconds)

def moveTo(x, y, seconds = 0.05):
    Mouse.position = (x, y)
    time.sleep(seconds)

def moveToAndClickButton(x, y, button, seconds = defaultTimeToWait):
    Mouse.position = (x, y)
    time.sleep(seconds)
    clickButton(button, seconds)

def clickButtonAndMoveTo(x, y, button, seconds = defaultTimeToWait):
    clickButton(button, seconds)
    Mouse.position = (x, y)
    time.sleep(seconds)

# ------------------ keyboard

def onlyPressKey(key):
    keyboard.press(key)

def onlyReleaseKey(key):
    keyboard.release(key)

def pressKey(key, seconds = defaultTimeToWait):
    keyboard.press_and_release(key)
    time.sleep(seconds)

def pressMultipleKeys(keys, seconds = defaultTimeToWait):
    for key in keys:
        keyboard.press(key)
    time.sleep(seconds)
    for key in keys:
        keyboard.release(key)

def writeWord(word, seconds = 0):
    pyautogui.write(word, interval = seconds)

def isPressed(key):
    return keyboard.is_pressed(key)

def waitForKey(key):
    while True:
        if isPressed(key):
            break
        
def getCurrentMousePos(coord = -1):
    if coord == -1:
        return Mouse.position
    elif coord == 0:
        return Mouse.position[0]
    return Mouse.position[1]