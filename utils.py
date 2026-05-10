import numpy as np
import cv2
from datetime import datetime
from pyzbar import pyzbar

def adaptive_threshold(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,251, 11)

def threshold(image):
    (_, binary_image) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image

def bilateral_filter(image):
    return cv2.bilateralFilter(image, 5, 75, 75)

def morphological(image):
    kernel = np.ones((3,3), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=3)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
    return image

def process(raw_image, allowance:int = 0):

        raw_image_array = np.frombuffer(raw_image.read(), np.uint8)
        
        image = cv2.imdecode(raw_image_array, cv2.IMREAD_COLOR)
    
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        barcode = pyzbar.decode(image)
        filename = barcode[0].data
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        hue_channel = hsv[:, :, 0]
        saturation_channel = hsv[:, :, 1]
        value_channel = hsv[:, :, 2]
        
        blurred = cv2.GaussianBlur(value_channel, (5,5), 0)

        (_, binary_image) = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        
        outline = max(contours, key=cv2.contourArea)
        perimeter = cv2.arcLength(outline, True)
        approx_corners = cv2.approxPolyDP(outline, 0.02 * perimeter, True)

        if len(approx_corners) == 4:
            box = approx_corners
        else:
            rect = cv2.minAreaRect(outline)
            box = cv2.boxPoints(rect)
            box = np.int32(box)
        
        mask = np.zeros(image.shape[:2], dtype = np.uint8)
        # draw contour of Edges unto the mask
        mask = cv2.drawContours(mask, [box], -1, 255, thickness=cv2.FILLED)

       

        no_bg = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        no_bg[:, :, 3] = mask

        x, y, w, h = cv2.boundingRect(outline)
        result = no_bg[y:y+h, x:x+w]
        result = cv2.rotate(result, cv2.ROTATE_90_COUNTERCLOCKWISE)

        return result, filename

def save(path, imagefile):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d")
    return cv2.imwrite(path, imagefile)
   


