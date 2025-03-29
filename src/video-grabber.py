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
        results['colors'] = []
        results[loc] = {
            'matches' : [],
        }
    return results



def get_matches_from_locations(areas, orb, target_features, target_images, game_image, results):

    game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) 
    game_image = crop_image(game_image, crop_fraction=0.8, preview=False)
    kp2, des2 = orb.get_features(game_image)
    # -=-=-=-=-=-=-=-=- Filter out Impossible Locations -=-=-=-=-=-=-=-=-
    locations = target_features.keys()
    location = None
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


            except Exception as e:
                print(f"[ERROR] {e}")
                print(target_images[loc][ref].shape)
                print(game_image.shape)

            if location:
                break
                
                
    return location


def fade_in(player, max_volume=101):
    for volume in range(0, max_volume, 5):
        player.audio_set_volume(volume)
        time.sleep(0.1)

def fade_out(player, max_volume=101):
    for volume in range(max_volume, -1, -5):
        player.audio_set_volume(volume)
        time.sleep(0.025)

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


    for i in range(1000):
        try:
            game_image = window.capture_as_image()
            cv2.imwrite(f'dataset/{i}.png', np.array(game_image))

            average_rgb = cv2.mean(np.array(game_image))[:3]  # returns (H, S, V, A) — we drop A
            results['colors'].append(average_rgb)
            print(f"[INFO] Average Colors {average_rgb}")

        except findwindows.ElementAmbiguousError or findwindows.ElementNotFoundError as e:
            print(f"[ERROR] {e}")
            continue

        # if Black Screen, Check for Features ('nexus')
        r, g, b = average_rgb[0:3]
        if r < 5 and g < 5 and b < 5:
            location = get_matches_from_locations(areas, orb, target_features, target_images, game_image, results)
        
        # Runic Tundra
        runic_tundra_upper = np.array([100, 120, 130])
        runic_tundra_lower = np.array([80, 100, 110])
        if np.all(average_rgb >= runic_tundra_lower) and np.all(average_rgb <= runic_tundra_upper):
            location = 'realm/runic-tundra'

        # Server Queue Screen
        queue_upper = np.array([48, 56, 48])
        queue_lower = np.array([46, 54, 46])
        if np.all(average_rgb >= queue_lower) and np.all(average_rgb <= queue_upper):
            location = 'nexus/queue'
            print("ALL!!!!! MATCH")

        sprite_forest_upper = np.array([68, 70, 95])
        sprite_forest_lower = np.array([55, 64, 80])
        if np.all(average_rgb >= sprite_forest_lower) and np.all(average_rgb <= sprite_forest_upper):
            location = 'realm/sprite-forest'

        haunted_hallows_upper = np.array([40,40,58])
        haunted_hallows_lower = np.array([30,30,50])
        if np.all(average_rgb >= haunted_hallows_lower) and np.all(average_rgb <= haunted_hallows_upper):
            location = 'realm/haunted-hallows'


        if not location:
            continue

        if 'nexus' in location:
            state = 'nexus'
        if 'realm' in location:
            state = 'realm'
        if 'dungeon' in location:
            state = 'dungeon'

     
        
        if location == last_location: 
            continue

        if player.get_state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.NothingSpecial]:
            player.play()

        last_location = location
        track = os.path.join(REF_DIR, location, areas[location].track)
        print(f"Track: {track}")
        media = vlc.Media(track)

        fade_out(player)
        player.set_media(media)
        player.play()
        fade_in(player)


    return results


        


if __name__ == '__main__':
    results = main()
    for loc, result in results.items():
        print(f"Result {result}")
        print(f"Location {loc}")
        plt.plot(result)
        plt.title(loc)
        plt.show()