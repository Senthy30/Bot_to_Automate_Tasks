import convertImageToText as conv
import ssProcessing as ss
import peripheralBehaviour as perb
import ctypes
import time
from PIL import Image
from pynput.mouse import Button

import cv2

# --------------------- declaration

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

valueItem = 0
maxValueItem = 100000

step = 0
currentTry = 0
maxTries = 10
streaks = (0, 0)
spaceBet = 72
yOffSet = 20

sizeIOffSet = (0, 377)
size3OffSet = (0, -90)
size4OffSet = (0, -50)
size5OffSet = (0, -15)
size6OffSet = (0, 20)

centerForI = (screensize[0] / 2 + sizeIOffSet[0], screensize[1] / 2 + sizeIOffSet[1])
centerFor3 = (screensize[0] / 2 + size3OffSet[0], screensize[1] / 2 + size3OffSet[1])
centerFor4 = (screensize[0] / 2 + size4OffSet[0], screensize[1] / 2 + size4OffSet[1])
centerFor5 = (screensize[0] / 2 + size5OffSet[0], screensize[1] / 2 + size5OffSet[1])
centerFor6 = (screensize[0] / 2 + size6OffSet[0], screensize[1] / 2 + size6OffSet[1])

typeItem = [[-1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0, 0, -1]]

currentImage = 0

# --------------------- predefine functions

def getRectangle():
    time.sleep(1)
    currentPos = (0, 0)

    print("Wait to capture...")
    perb.waitForKey('enter')

    currentPos = perb.getCurrentMousePos()
    print(currentPos)
    time.sleep(0.5)

    perb.waitForKey('enter')

    diferencePos = (perb.getCurrentMousePos(0) - currentPos[0], perb.getCurrentMousePos(1) - currentPos[1])
    print(diferencePos)

def intro():
    print("Press enter to start...")
    perb.waitForKey('enter')
    print("Starting...")

def getPixelOfPos(x, y):
    Color = ss.getPixelByCoordsFromScreen(centerFor6[0] + x * spaceBet, centerFor6[1] + y * spaceBet)

    return Color

def getPointByXY(x, y):
    sthOffSet = 4
    return ((centerForI[0] - (4 - x) * spaceBet, centerForI[1] - (3 - y) * spaceBet - yOffSet * (y != 3) - sthOffSet * (y == 3)))

def findTypeItems():
    currentImage = 1
    for currentR in range(0, 4):
        for currentC in range(0, 9):
            if typeItem[currentR][currentC] == -1:
                continue
            typeItem[currentR][currentC] = 0

    for currentR in range(0, 4):
        for currentC in range(0, 9):
            if typeItem[currentR][currentC] == -1:
                continue
            
            middlePosition = getPointByXY(currentC, currentR)
            image = ss.getScreenshotAfterRGBChanges(middlePosition[0] - 5, middlePosition[1] - 5, 10, 10)
            image = Image.fromarray(image)
            Color = image.getpixel((5, 5))

            if Color == (255, 255, 255):
                isEmpty = True
                for i in range(0, 9):
                    if isEmpty == False:
                        break
                    for j in range(0, 9):
                        if image.getpixel((i, j)) != (255, 255, 255):
                            isEmpty = False
                            break
                if isEmpty == True:
                    typeItem[currentR][currentC] = 0
                else:
                    typeItem[currentR][currentC] = 4
            elif Color == (0, 255, 255):
                typeItem[currentR][currentC] = 1
            else:
                typeItem[currentR][currentC] = 2

def getPosByInv(x, y, val):
    ans = (0, 0)
    if val == 3:
        ans = centerFor3
    elif val == 4:
        ans = centerFor4
    elif val == 5:
        ans = centerFor5
    elif val == 6:
        ans = centerFor6
    return (ans[0] + x * spaceBet, ans[1] + y * spaceBet)

def moveItemToPos(x, y):
    perb.clickButtonAndMoveTo(centerFor6[0] + x * spaceBet, centerFor6[1] + y * spaceBet, Button.left)
    perb.clickButton(Button.left)

def findValueInTypeItems(val):
    cnt = 0
    for currentR in range(0, 4):
        for currentC in range(0, 9):
            if typeItem[currentR][currentC] == val:
                cnt += 1
    return cnt

def getPosOfTypeItem(val):
    for currentR in range(0, 4):
        for currentC in range(0, 9):
            if typeItem[currentR][currentC] == val:
                return (currentR, currentC)

def moveItem(itemPos, finalPos):
    middlePosition = getPointByXY(itemPos[1], itemPos[0])
    perb.moveTo(middlePosition[0], middlePosition[1])
    moveItemToPos(finalPos[1], finalPos[0])
    typeItem[itemPos[0]][itemPos[1]] = 0
    perb.moveTo(0, 0)

def restartCraftingMenu(rectangle, menuName):
    timeToSlepp = 0.1

    perb.pressKey('esc')
    while True:
        if conv.getTextFromCoords(rectangle[0], rectangle[1], rectangle[2], rectangle[3], 150).find(menuName) == -1:
            break
    time.sleep(timeToSlepp)

    perb.clickButton(Button.right)

    while True:
        if conv.getTextFromCoords(635, 113, 182, 41, 150).find('SkyBlock') != -1:
            break

    time.sleep(timeToSlepp)
    dest = getPosByInv(0, -2, 6)
    perb.moveToAndClickButton(dest[0], dest[1], Button.left)

    while True:
        if conv.getTextFromCoords(636, 114, 116, 38, 150).find('Craft') != -1:
            break

    perb.moveTo(0, 0)

def fillWithItem(typeItem, rectangle, menuName, limitValue):
    numberOfFreeSpaces = findValueInTypeItems(0)

    dest = getPointByXY(2 - typeItem, 3)
    perb.moveToAndClickButton(dest[0], dest[1], Button.right)

    while True:
        if conv.getTextFromCoords(rectangle[0], rectangle[1], rectangle[2], rectangle[3], 150).find(menuName) != -1:
            break

    if typeItem == 1:
        dest = getPosByInv(1, -1, 4)
        perb.moveTo(dest[0], dest[1])
    else:
        dest = getPosByInv(1, -2, 4)
        perb.moveTo(dest[0], dest[1])

    if numberOfFreeSpaces <= limitValue:
        perb.clickButton(Button.left)
        time.sleep(0.4)
    else:
        for i in range(0, limitValue):
            perb.clickButton(Button.right)

    restartCraftingMenu(rectangle, menuName)

def tryToMoveItemAndRepart(itemType, pos):
    moveItem(getPosOfTypeItem(itemType), pos)

# --------------------- step functions

def executeStep__0():
    ColorToVerify = (255, 28, 43)
    Color = ss.getPixelByCoordsFromScreen(centerFor6[0] - 4 * spaceBet, centerFor6[1] - 2 * spaceBet)
    if ss.inRangeOf(Color, ColorToVerify):
        perb.moveToAndClickButton(centerFor6[0] - 4 * spaceBet, centerFor6[1] - 3 * spaceBet, Button.left)
        perb.moveTo(0, 0)

        return True
    
    return False

def executeStep_0():
    findTypeItems()

    if findValueInTypeItems(1) < 1:
        fillWithItem(1, (636, 188, 98, 36), 'Agro', 7)
        time.sleep(0.2)
        findTypeItems()

    if findValueInTypeItems(2) < 4:
        fillWithItem(2, (636, 188, 98, 36), 'Ench', 36)
        time.sleep(0.2)
        findTypeItems()

    tryToMoveItemAndRepart(1, (-3, -2))
    tryToMoveItemAndRepart(2, (-4, -2))
    tryToMoveItemAndRepart(2, (-3, -1))
    tryToMoveItemAndRepart(2, (-2, -2))
    tryToMoveItemAndRepart(2, (-3, -3))

    startTime = time.time()
    wasRestarted = False
    while getPixelOfPos(1, -3) == (207, 0, 0):
        if time.time() - startTime > 2:
            restartCraftingMenu((636, 114, 116, 38), 'Craft')
            wasRestarted = True
            break
        if perb.isPressed('r') == True:
            break
        time.sleep(0.1)

    if wasRestarted == True:
        return

    perb.moveTo(centerFor6[0] + spaceBet, centerFor6[1] - 3 * spaceBet)
    perb.onlyPressKey('shift')
    time.sleep(0.05)
    perb.onlyPressButton(Button.left)
    time.sleep(0.1)
    perb.onlyReleaseButton(Button.left)
    perb.onlyReleaseKey('shift')

    perb.moveTo(0, 0)

# --------------------- commands

intro()

while True:
    if perb.isPressed('r') == True:
        break

    globals()["executeStep_" + str(step)]()

    time.sleep(0.2)