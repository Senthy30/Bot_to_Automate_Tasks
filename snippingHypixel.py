from pynput.mouse import Button
import convertImageToText as conv
import ssProcessing as ss
import peripheralBehaviour as perb
import ctypes
import time

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

size3OffSet = (0, -90)
size4OffSet = (0, -50)
size6OffSet = (0, 20)

centerFor3 = (screensize[0] / 2 + size3OffSet[0], screensize[1] / 2 + size3OffSet[1])
centerFor4 = (screensize[0] / 2 + size4OffSet[0], screensize[1] / 2 + size4OffSet[1])
centerFor6 = (screensize[0] / 2 + size6OffSet[0], screensize[1] / 2 + size6OffSet[1])

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

# --------------------- step functions

def executeStep_0():
    ColorToVerify = (255, 28, 43)
    Color = ss.getPixelByCoordsFromScreen(centerFor6[0] - 4 * spaceBet, centerFor6[1] - 2 * spaceBet)
    if ss.inRangeOf(Color, ColorToVerify):
        perb.moveToAndClickButton(centerFor6[0] - 4 * spaceBet, centerFor6[1] - 3 * spaceBet, Button.left)
        perb.moveTo(0, 0)

        return True
    
    return False

def executeStep_1():
    ColorToVerify = (139, 139, 139)
    Color = ss.getPixelByCoordsFromScreen(centerFor6[0] - 2 * spaceBet, centerFor6[1] - 4 * spaceBet)
    if ss.inRangeOf(Color, ColorToVerify):
        perb.moveToAndClickButton(centerFor6[0] - 4 * spaceBet, centerFor6[1] - 1 * spaceBet, Button.left)
        perb.moveTo(0, 0)

        return True

    return False

def executeStep_2():
    ColorToVerify = (139, 139, 139)
    Color = ss.getPixelByCoordsFromScreen(centerFor6[0] - 2 * spaceBet, centerFor6[1] - 4 * spaceBet)
    if ss.notInRangeOf(Color, ColorToVerify):
        perb.moveTo(centerFor6[0] - 2 * spaceBet + streaks[0] * spaceBet, centerFor6[1] - 4 * spaceBet + streaks[1] * spaceBet)
        return True

    return False

def executeStep_3():
    global valueItem, step, streaks

    text = conv.getTextFromCoords(perb.getCurrentMousePos(0) + 0.5 * spaceBet, perb.getCurrentMousePos(1) + 2.7 * spaceBet, 2 * spaceBet, 0.6 * spaceBet, 45)
    if text.find('Buyer') != -1:
        streaks = (streaks[0] + 1, streaks[1])
        if streaks[0] == 6:
            streaks = (0, streaks[1] + 1)
        step = -1
        
        return True

    text = conv.getTextFromCoords(perb.getCurrentMousePos(0) + 3.7 * spaceBet, perb.getCurrentMousePos(1) + 2.7 * spaceBet, 3 * spaceBet, 0.6 * spaceBet, 40)
    valueItem = 0

    if text.find('soon') != -1:
        step -= 1

        return True

    for letter in text:
        if letter == 'c':
            break 
        if ord(letter) >= 48 and ord(letter) <= 57:
            valueItem = valueItem * 10 + ord(letter) - 48
    
    print("value item:", valueItem)

    if valueItem > 0:
        if valueItem > maxValueItem:
            step = -1
            streaks = (0, 0)
        else:
            perb.clickButton(Button.left)
            perb.moveTo(0, 0)
            streaks = (streaks[0] + 1, streaks[1])
            if streaks[0] == 6:
                streaks = (0, streaks[1] + 1)

        return True

    return False

def executeStep_4():
    ColorToVerify = (222, 222, 0)
    Color = ss.getPixelByCoordsFromScreen(centerFor6[0], centerFor6[1] - 2 * spaceBet)
    if ss.inRangeOf(Color, ColorToVerify):
        perb.moveToAndClickButton(centerFor6[0], centerFor6[1] - 2 * spaceBet, Button.left)
        perb.moveTo(0, 0)

        return True

    return False

def executeStep_5():
    ColorToVerify = (33, 36, 18)
    Color = ss.getPixelByCoordsFromScreen(centerFor3[0] - 2 * spaceBet, centerFor3[1] - 1 * spaceBet)
    if ss.inRangeOf(Color, ColorToVerify):
        perb.moveToAndClickButton(centerFor3[0] - 2 * spaceBet, centerFor3[1] - 1 * spaceBet, Button.left)
        perb.moveTo(0, 0)

        return True

    return False

def executeStep_6():
    ColorToVerify = (62, 26, 20)
    Color = ss.getPixelByCoordsFromScreen(centerFor3[0] + 2 * spaceBet, centerFor3[1] - 1 * spaceBet)
    if ss.notInRangeOf(Color, ColorToVerify):
        time.sleep(0.1)
        perb.pressKey('t')
        perb.writeWord('/ah')
        perb.pressKey('enter')

        return True

    return False

def executeStep_7():
    global step

    Color = ss.getPixelByCoordsFromScreen(centerFor4[0] - 2 * spaceBet, centerFor4[1] - 2 * spaceBet)
    if ss.inRangeOf(Color, (102, 91, 30)):
        perb.moveToAndClickButton(centerFor4[0] - 2 * spaceBet, centerFor4[1] - 2 * spaceBet, Button.left)
        perb.moveTo(0, 0)
        step = -1

        return True

    return False

# --------------------- commands

intro()

while True:
    if perb.isPressed('r') == True:
        break

    done = globals()["executeStep_" + str(step)]()

    if done == True:
        step += 1
    else:
        currentTry += 1

    if currentTry > maxTries:
        perb.pressKey('esc')
        step = 6
        currentTry = 0

    time.sleep(0.2)