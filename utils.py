import numpy as np
import cv2

def adaptive_threshold(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,251, 11)

def threshold(image):
    (_, binary_image) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image

def bilateral_filter(image):
    return cv2.bilateralFilter(image, 5, 75, 75)

def morphological(image):
    kernel = np.ones((5,5), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)
    return image

def process(raw_image, allowance:int = 10):
        

        raw_image_array = np.frombuffer(raw_image.read(), np.uint8)
        image = cv2.imdecode(raw_image_array, cv2.IMREAD_COLOR)
    
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        hue_channel = hsv[:, :, 0]
        saturation_channel = hsv[:, :, 1]
        value_channel = hsv[:, :, 2]
        
        blurred = cv2.bilateralFilter(saturation_channel, 5, 75, 75)
        
        binary_image = adaptive_threshold(blurred)

        binary_image = morphological(binary_image)

        mask = np.zeros(image.shape[:2], dtype = np.uint8)

        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        outline = max(contours, key = cv2.contourArea)

        x, y, w, h = cv2.boundingRect(outline)
        
        allowance = int(allowance * w)
        x -= allowance 
        y -= allowance
        w += 2 * allowance
        h += 2 * allowance

        #cv2.rectangle(mask, (x, y), (x + w, y + h), 255, thickness=cv2.FILLED)

        #no_bg = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        #no_bg[:, :, 3] = mask
    
        final = image[y:y+h, x:x+w]
        return final

def save(path, imagefile):
    return cv2.imwrite(path, imagefile)
   
