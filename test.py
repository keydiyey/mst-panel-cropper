from pyzbar import pyzbar
import numpy as np
import cv2
import zxingcpp
import easyocr

trial_image = "./testcase/IMG_6096.JPG"

#raw_image_array = np.frombuffer(trial_image.read(), np.uint8)
        
#image = cv2.imdecode(raw_image_array, cv2.IMREAD_COLOR)

image = cv2.imread(trial_image)
image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
h, w = image.shape[:2]
y = int(h * 0.0)
h = int(h * 0.08)
x = int(w * 0.40)
w = int(w * 0.60)


barcode_crop = image[y:h, x:w]
barcode_crop = cv2.cvtColor(barcode_crop, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
equalized = clahe.apply(barcode_crop)
barcode = zxingcpp.read_barcodes(equalized)
if len(barcode) != 0:
    print(barcode[0].text)
else:
    reader = easyocr.Reader(["en"])
    result = reader.readtext(equalized)
    for (bbox, text, prob) in result:
        print(f"Text = {text}  Prob: {prob}")
        ID = text.split("-")
        sampleid = ID[1:]
        print(sampleid)

    print("Barcode not found!")
cv2.imshow('Cropped Barcode', equalized)

# 3. Wait indefinitely until you press any key on your keyboard
cv2.waitKey(0)

# 4. Clean up and close the window
cv2.destroyAllWindows()
