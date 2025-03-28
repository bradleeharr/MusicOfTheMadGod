import cv2
import os
import numpy as np
import pyaudio
import time


import vlc



from pywinauto import Desktop, Application

# Crop images to save processing power
def crop_image(game_image, crop_fraction=0.30, preview=False):


    height, width = game_image.shape[:2]
    ch = int(height * crop_fraction)
    cw = int(width * crop_fraction)
    y1 = (height - ch) // 2
    x1 = (width - cw) // 2

    if preview:
        preview = game_image.copy()
        cv2.rectangle(preview, (x1, y1), (x1 + cw, y1 + ch), (0, 255, 0), 2)
        cv2.imshow("Crop Region", preview)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    return game_image[y1:y1+ch, x1:x1+ch]
    


class Area:
    def __init__(self, track: str, tolerance: float):
        self.track = track
        self.tolerance = tolerance

def main():
    app = Application(backend="uia").connect(title="RotMGExalt")
    app.RotMGExalt.set_focus()
    window = app.window(title="RotMGExalt")
    areas = {
        'nexus' :          Area('12_Hadenfeer.flac', 0.5),
        'realm-novice' :   Area('02_Odyssey.flac', 0.5),
        'sprite' :         Area('15_Arc_Sancts.flac', 0.5),
        'deep-sea-abyss' : Area('11_Mechanical_Ambivalence.flac', 0.5),
    }
    player = vlc.MediaPlayer()

    location = None
    last_location = None

    # Load all images into memory. This saves time to do it beforehand rather than repeatedly open the image file. 
    target_images = {}
    for loc in areas.keys():
        dir = f'images/ref/{loc}/'
        for ref in os.listdir(dir):
            if dir not in target_images.keys():
                target_images[loc] = {}
            target_images[loc][ref] = cv2.imread(os.path.join(dir, ref))


    for i in range(6000):
        game_image = window.capture_as_image()
        game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) 
        game_image = crop_image(game_image, 0.4, preview=False)

        for loc in target_images.keys():
            for ref in target_images[loc].keys():
                try:
                    # Try with opencv template matching
                    target_image = target_images[loc][ref]
                    result = cv2.matchTemplate(game_image, target_image, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(result)

                    threshold = 0.6
                    
                    if max_val > threshold * 0.2:
                        print(f"[DEBUG] {ref}: {max_val}")

                    if max_val >= areas[loc].tolerance:
                        x, y =  max_loc
                        location = loc
                        print(f"[DEBUG] {ref} Match found at ({x}, {y})")
                except Exception as e:
                    print(f"[ERROR] {e}")
                    print(game_image.shape)
                    print(target_image.shape)

                if location:
                    break

            

        
        if location != last_location: 
            last_location = location
            track = f"tracks/{areas[location].track}"
            print(f"Track: {track}")
            media = vlc.Media(track)
            player.set_media(media)
            player.play()

            if not location:
                player.stop()

if __name__ == '__main__':
    main()