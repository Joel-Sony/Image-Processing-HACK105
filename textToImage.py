import easyocr
import cv2

def imagetotext(image_path):
    image_path = image_path[0]
    reader = easyocr.Reader(['en','hi'])  # this needs to run only once to load the model into memory
    image = cv2.imread(image_path)

    returnresult = []
    result = reader.readtext(image)
    for i in result:
        returnresult.append(i[1])
    return returnresult
