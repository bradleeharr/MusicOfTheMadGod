import cv2
import os
import numpy as np
import time
import win32ui
import sys

from pywinauto import Desktop, Application
from pywinauto import findwindows

import utility as utility

from orb import Orb
from areas import Areas
from crossfader import Crossfader

import matplotlib.pyplot as plt

REF_DIR ='ref/' # Reference directory that contains images and audio files

def load_images_and_features(ref_dir, orb, areas):
    target_features = {}
    target_images = {}
    for loc in areas.keys():
        dir = os.path.join(ref_dir, loc)
        if not os.path.exists(dir):
            continue
        for ref_file in os.listdir(dir):
            if not ref_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
            if dir not in target_features.keys():
                target_features[loc] = {}
                target_images[loc] = {}
            target_images[loc][ref_file] = cv2.imread(os.path.join(dir, ref_file))
            target_features[loc][ref_file] = orb.get_features(cv2.imread(os.path.join(dir, ref_file)))

    return target_images, target_features






def get_matches_from_locations(areas, orb, target_features, target_images, game_image, results):

    game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) 
    game_image = utility.crop_image(game_image, crop_fraction=0.8, preview=False)
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
                    start = time.time()
                    matches = orb.bf.match(des1, des2)
                    end = time.time()
                    matches = sorted(matches, key=lambda x: x.distance)

                    # print(f"[DEBUG] found {len(matches)} matches for loc {loc}")

                    results[loc]['matches'].append(len(matches))

                    print(f"[DEBUG] {loc} - Matches {len(matches)} - Time: {round(end - start, 3)}")

                    if len(matches) > areas[loc].threshold:
                        print(f"[MATCH] Object matches with {len(matches)} for loc {loc}")
                        print(f"Should Play {areas[loc].tracks}")
                        location = loc
                        # matched_vis = orb.draw_matches(target_images[loc][ref], kp1, game_image, kp2, matches)
                        # cv2.imshow("ORB Match", matched_vis)

            except Exception as e:
                print(f"[ERROR] {e}")
                print(target_images[loc][ref].shape)
                print(game_image.shape)

            if location:
                break
                
                
    return location

RUN = 'PROD'

def get_app():
    try: 
        app = Application(backend="uia").connect(title="RotMGExalt")
        return app
    except Exception as e: 
        print(f"[ERROR] {e}")
        return None


def main():
    app = None
    while not app:
        app = get_app()

    orb = Orb()
    app.RotMGExalt.set_focus()
    window = app.window(title="RotMGExalt")

    [print(f"[DEBUGEEE] {sys.argv}") for i in range(10)]
    if len(sys.argv) > 1: 
        location = sys.argv[1]
        last_location = sys.argv[1]
        print(f"location {location}")
    else:
        location = None
        last_location = None
    state = 'nexus'
    

    # Get all track filepaths and cache
    areas = Areas().update(REF_DIR)

    # Create empty results list for each area
    results = utility.create_results_empty(areas)

    # Intialize playback and crossfader object with list of all tracks to load
    crossfader = Crossfader(areas)
    time.sleep(1)

    # Load all images into memory. This saves time to do it beforehand rather than repeatedly open the image file. 
    target_images, target_features = load_images_and_features(REF_DIR, orb, areas)




    for i in range(10000):
        if last_location and not crossfader.channel1.get_busy():
            print("Song ended. Replaying it...")
            crossfader.crossfade(last_location)
            crossfader.replay()
        
        # Capture image to detect song logic
        try:
            game_image = window.capture_as_image()
            if RUN == 'DEBUG':
                cv2.imwrite(f'dataset/{i}.png', np.array(game_image))

            average_rgb = np.array(cv2.mean(np.array(game_image))[:3])  # returns (H, S, V, A) — we drop A
            results['colors'].append(average_rgb)
        except win32ui.error as e:
            print(f"[ERROR] {e}")
            app = get_app()
            app.RotMGExalt.set_focus()
            window = app.window(title="RotMGExalt")
        except findwindows.ElementAmbiguousError or findwindows.ElementNotFoundError as e:
            print(f"[ERROR] {e}")
            continue

        # if Black Screen, Check for Features ('nexus')
        r, g, b = average_rgb[0:3]
        if r < 5 and g < 5 and b < 5:
            location = get_matches_from_locations(areas, orb, target_features, target_images, game_image, results)
        
        # If in realm, do some detection based on the color of each
        if (last_location and 'realm' in last_location) or not location:
            for location_name in areas:
                # If either are undefined, we'll continue 
                if areas[location_name].lower_rgb is None or areas[location_name].upper_rgb is None:
                    continue
                if np.all(average_rgb >= areas[location_name].lower_rgb) and np.all(average_rgb <= areas[location_name].upper_rgb): 
                    location = location_name

        if not location:
            print(f"[INFO] Average Colors {average_rgb.astype(int)}: Location = {location}. Last Location = {last_location}")
            continue
        else:
            print(f"[INFO] Average Colors {average_rgb.astype(int)}: Location = {location}. Matches = {results[location]}. Last Location = {last_location}")


        if 'nexus' in location:
            state = 'nexus'
        if 'realm' in location:
            state = 'realm'
        if 'dungeon' in location:
            state = 'dungeon'

     
        
        if location == last_location: 
            continue

        last_location = location
        print('test!')
        print(f"Track: {areas[location].tracks}")
        
        crossfader.crossfade(location)


    return results


        


if __name__ == '__main__':
    results = main()
    for loc, result in results.items():
        print(f"Result {result}")
        print(f"Location {loc}")
        plt.plot(result)
        plt.title(loc)
        plt.show()