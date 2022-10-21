import tesserocr
import cv2
import numpy
import ssProcessing as ss
from PIL import Image

stringPath = "C:/Users/crang/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/tesserocr/tessdata"
apiMC = tesserocr.PyTessBaseAPI(path=stringPath, psm=6, lang="mc")

#currentImage = 0

def getTextFromImage(image, grade = 50):
    global currentImage

    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, grade, 255, cv2.THRESH_BINARY)[1]
    #cv2.imwrite('ss/ss' + str(currentImage) + '.png', image)
    currentImage += 1
    image = Image.fromarray(image)
    
    apiMC.SetImage(image)
    text = apiMC.GetUTF8Text()

    return text

def getTextFromCoords(x, y, w, h, grade = 50):
    image = ss.getScreenshot(x, y, w, h)
    text = getTextFromImage(image, grade)

    return text