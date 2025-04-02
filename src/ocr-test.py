import easyocr
import cv2
import os
import numpy as np
from areas import Areas
import time

reader = easyocr.Reader(['en'], gpu=False)


ref_dir = 'ref/'
target_images = {}
areas = Areas().update(ref_dir)
for loc in areas.keys():
    dir = os.path.join(ref_dir, loc)
    for ref_file in os.listdir(dir):
        if not ref_file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
        if dir not in target_images.keys():
            target_images[loc] = {}
        target_images[loc] = cv2.imread(os.path.join(dir, ref_file))



# Crop images to save processing power
def crop_image(image, crop_fraction=1.0, preview=False):
    height, width = image.shape[:2]
    ch = int(height * crop_fraction)
    cw = int(width * crop_fraction)
    y1 = (height - ch) // 2
    x1 = (width - cw) // 2

    if preview:
        preview = image.copy()
        cv2.rectangle(preview, (x1, y1), (x1 + cw, y1 + ch), (0, 255, 0), 2)
        cv2.imshow("Crop Region", preview)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    return image[y1:y1+ch, x1:x1+ch]





for loc, image in target_images.items():
    image = np.array(image)

    cropped = crop_image(image, 0.4, preview=(False))
    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    start = time.time()
    results = reader.readtext(cropped_rgb)
    end = time.time()

    print("=== OCR Results ===")
    for (bbox, text, confidence) in results:
        print(bbox)
        print(f"Detected text: '{text}' (Confidence: {confidence:.2f}) Actual: {loc} Time: {end - start}")
        
