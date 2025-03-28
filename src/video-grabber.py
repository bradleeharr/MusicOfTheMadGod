import cv2
import os
import numpy as np
import pyaudio
import time


import vlc



from pywinauto import Desktop, Application

from areas import areas
# Crop images to save processing power
def crop_image(game_image, crop_fraction=1.0, preview=False):


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



state = 'realm'


class Orb:
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=225)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    def get_features(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.orb.detectAndCompute(gray, None)
    
    def draw_matches(self, img1, kp1, img2, kp2, matches):
        return cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)
    



def main():
    app = Application(backend="uia").connect(title="RotMGExalt")
    orb = Orb()

    app.RotMGExalt.set_focus()
    window = app.window(title="RotMGExalt")

    player = vlc.MediaPlayer()

    location = None
    last_location = None

    # Load all images into memory. This saves time to do it beforehand rather than repeatedly open the image file. 
    target_features = {}
    target_images = {}
    for loc in areas.keys():
        dir = os.path.join('images/ref', loc)
        for ref in os.listdir(dir):
            if dir not in target_features.keys():
                target_features[loc] = {}
                target_images[loc] = {}
            target_images[loc][ref] = cv2.imread(os.path.join(dir, ref))
            target_features[loc][ref] = orb.get_features(cv2.imread(os.path.join(dir, ref)))

    # Get all track filepaths and cache
    for loc in areas.keys():
        dir = os.path.join('tracks/', loc)
        for ref in os.listdir(dir):
            areas[loc].track = ref
            print(f"[DEBUG] Set Area {loc} Track to {ref}")

    
    while True:
        game_image = window.capture_as_image()
        game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) 
        game_image = crop_image(game_image, crop_fraction=0.8, preview=False)
        
        kp2, des2 = orb.get_features(game_image)

        for loc in target_features.keys():
            for ref in target_features[loc].keys():
                try:
                    print(loc)
                    kp1, des1 = target_features[loc][ref]

                    # Try with opencv ORB matching
                    if des1 is not None and des2 is not None:
                        matches = orb.bf.match(des1, des2)
                        matches = sorted(matches, key=lambda x: x.distance)

                        print(f"[DEBUG] found {len(matches)} matches for loc {loc}")

                        threshold = 100 # threshold is number of matches
                        if len(matches) > areas[loc].threshold:
                            print(f"[MATCH] Object matches with {len(matches)} for loc {loc}")
                            print(f"Should Play {areas[loc].track}")
                            location = loc
                            matched_vis = orb.draw_matches(target_images[loc][ref], kp1, game_image, kp2, matches)
                            cv2.imshow("ORB Match", matched_vis)
                            cv2.waitKey(1)  # Replace with 0 to pause
                except Exception as e:
                    print(f"[ERROR] {e}")
                    print(target_images[loc][ref].shape)
                    print(game_image.shape)

                if location:
                    break

        

        if state == 'realm' and location.startswith('realm') and location != last_location:
            pass
            # If in the realm, you can go anywhere
        
        if state == 'dungeon':
            pass
            # If in a dungeon, you can only go to the realm or to nexus
        
        if state == 'nexus':
            pass
            # If in the nexus, you can only go to the vault, pet yard, tinkerer area, or guild hall
        
        if location != last_location: 
            last_location = location
            track = f"tracks/{location}/{areas[location].track}"
            print(f"Track: {track}")
            media = vlc.Media(track)
            player.set_media(media)
            player.play()
        elif player.get_state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.NothingSpecial]:
            player.play()
        if not location:
            player.stop()

if __name__ == '__main__':
    main()