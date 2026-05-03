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
    kernel = np.ones((3,3), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=3)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
    return image

def process(raw_image, allowance:int = 0):
        raw_image_array = np.frombuffer(raw_image.read(), np.uint8)
        image = cv2.imdecode(raw_image_array, cv2.IMREAD_COLOR)
    
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        hue_channel = hsv[:, :, 0]
        saturation_channel = hsv[:, :, 1]
        value_channel = hsv[:, :, 2]
        
        blurred = cv2.GaussianBlur(value_channel, (5,5), 0)
        edges = threshold(blurred)

        #edges = cv2.Canny(blurred, 50, 150)

        kernel = np.ones((3,3), np.uint8)
        binary_image = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)

        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        if not contours:
            return image

        outline = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(outline)

     
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
        
        masked = cv2.bitwise_and(image, image, mask=mask)
    
        result = image[y:y+h, x:x+w]
        result = cv2.rotate(result, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return result

def save(path, imagefile):
    return cv2.imwrite(path, imagefile)
   
