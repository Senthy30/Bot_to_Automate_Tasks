from email.mime import image
import cv2
import numpy
from mss import mss
from PIL import Image

sct = mss()
captureScreen = {'top': 2000, 'left': 2000, 'width': 2000, 'height': 2000}

def updateCaptureScreen(x, y, w, h):
    global captureScreen
    captureScreen = {'top': int(y), 'left': int(x), 'width': int(w), 'height': int(h)}

def getScreenshot(x, y, w, h):
    updateCaptureScreen(x, y, w, h)
    image = sct.grab(captureScreen)

    return image

def getPixelByCoordsFromImage(image, x, y):
    image = Image.frombytes("RGB", image.size, image.bgra, "raw", "BGRX")
    
    return image.getpixel((x, y))

def getPixelByCoordsFromScreen(x, y):
    image = getScreenshot(x - 2, y - 2, 5, 5)
    image = Image.frombytes("RGB", image.size, image.bgra, "raw", "BGRX")
    
    return image.getpixel((3, 3))

def inRangeOf(x, y, tolerence = 3):
    for i in range(0, 3):
        if y[i] - tolerence > x[i] or y[i] + tolerence < x[i]:
            return False
    
    return True

def notInRangeOf(x, y, tolerence = 3):
    for i in range(0, 3):
        if y[i] - tolerence <= x[i] and y[i] + tolerence >= x[i]:
            return False
    
    return True

def getScreenshotAfterRGBChanges(x, y, w, h, grade = 80):
    image = getScreenshot(x - w // 2, y - h // 2, w, h)
    
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGBA2RGB)
    image = cv2.threshold(image, grade, 255, cv2.THRESH_BINARY)[1]

    return image
