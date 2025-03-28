import cv2
import os
import numpy as np
import pyaudio
import time
import vlc

from pywinauto import Desktop, Application
from pywinauto import findwindows

from areas import Areas


import matplotlib.pyplot as plt


REF_DIR ='ref/' # Reference directory that contains images and audio files



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

class Orb:
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=225)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    def get_features(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.orb.detectAndCompute(gray, None)
    
    def draw_matches(self, img1, kp1, img2, kp2, matches):
        return cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)
    

#Filters out biomes when they do not need to be considered outside of the realm
def filter_realm_locations_except_realm_novice(locations):
    ret = []
    for loc in locations:
        if 'realm' not in loc or 'realm/novice' in loc:
            ret.append(loc)
    return ret

def load_images_and_features(ref_dir, orb, areas):
    target_features = {}
    target_images = {}
    for loc in areas.keys():
        dir = os.path.join(ref_dir, loc)
        for ref_file in os.listdir(dir):
            if not ref_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
            if dir not in target_features.keys():
                target_features[loc] = {}
                target_images[loc] = {}
            target_images[loc][ref_file] = cv2.imread(os.path.join(dir, ref_file))
            target_features[loc][ref_file] = orb.get_features(cv2.imread(os.path.join(dir, ref_file)))

    return target_images, target_features


def create_results_empty(areas):
    results = {}
    for loc in areas.keys():
        results['hsvs'] = []
        results[loc] = {
            'matches' : [],
        }
    return results


def main():
    
    app = None
    while not app:
        try: 
            app = Application(backend="uia").connect(title="RotMGExalt")
        except Exception as e: 
            print(f"[ERROR] {e}")
            pass

    orb = Orb()
    app.RotMGExalt.set_focus()
    window = app.window(title="RotMGExalt")
    player = vlc.MediaPlayer()

    location = None
    last_location = None
    state = 'nexus'
    

    # Get all track filepaths and cache
    areas = Areas().update(REF_DIR)

    # Create empty results list for each area
    results = create_results_empty(areas)


    # Load all images into memory. This saves time to do it beforehand rather than repeatedly open the image file. 
    target_images, target_features = load_images_and_features(REF_DIR, orb, areas)

    for i in range(100):
        try:
            game_image = window.capture_as_image()

            hsv_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2HSV)
            hue_hist = cv2.calcHist([hsv_image], [0], None, [180], [0, 180])
            sat_hist = cv2.calcHist([hsv_image], [1], None, [256], [0, 256])
            val_hist = cv2.calcHist([hsv_image], [2], None, [256], [0, 256])
            average_hsv = cv2.mean(hsv_image)[:3]  # returns (H, S, V, A) — we drop A
            results['hsvs'].append(average_hsv)
            print(f"[INFO] Average HSVs {average_hsv}")

        except findwindows.ElementAmbiguousError or findwindows.ElementNotFoundError as e:
            print(f"[ERROR] {e}")
            continue

        game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) 
        game_image = crop_image(game_image, crop_fraction=0.8, preview=False)
        kp2, des2 = orb.get_features(game_image)
        
        
        # -=-=-=-=-=-=-=-=- Filter out Impossible Locations -=-=-=-=-=-=-=-=-
        locations = target_features.keys()

        # If not in realm, the only realm biome you can go into is the entry level (novice)
        # if state != 'realm':
        #    locations = filter_realm_locations_except_realm_novice(locations)      
        # If in the realm, you can go anywhere
        # else:
        #   pass


        for loc in locations:
            for ref in target_features[loc].keys():
                try:
                    kp1, des1 = target_features[loc][ref]

                    # Try with opencv ORB matching
                    if des1 is not None and des2 is not None:
                        matches = orb.bf.match(des1, des2)
                        matches = sorted(matches, key=lambda x: x.distance)

                        # print(f"[DEBUG] found {len(matches)} matches for loc {loc}")

                        results[loc]['matches'].append(len(matches))
                        if len(matches) > areas[loc].threshold:
                            print(f"[MATCH] Object matches with {len(matches)} for loc {loc}")
                            print(f"Should Play {areas[loc].track}")
                            location = loc
                            matched_vis = orb.draw_matches(target_images[loc][ref], kp1, game_image, kp2, matches)
                            cv2.imshow("ORB Match", matched_vis)
                            cv2.waitKey(1)  # Replace with 0 to pause

                            if 'nexus' in loc:
                                state = 'nexus'
                            if 'realm' in loc:
                                state = 'realm'
                            if 'dungeon' in loc:
                                state = 'dungeon'

                except Exception as e:
                    print(f"[ERROR] {e}")
                    print(target_images[loc][ref].shape)
                    print(game_image.shape)

                if location:
                    break

        if not location:
            continue
        
        if location == last_location: 
            continue

        if player.get_state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.NothingSpecial]:
            player.play()

        last_location = location
        track = os.path.join(REF_DIR, location, areas[location].track)
        print(f"Track: {track}")
        media = vlc.Media(track)
        player.set_media(media)
        player.play()


    return results


        


if __name__ == '__main__':
    results = main()
    for loc, result in results.items():
        print(f"Result {result}")
        print(f"Location {loc}")
        plt.plot(result)
        plt.title(loc)
        plt.show()