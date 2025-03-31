import cv2
import os
import numpy as np
import pyaudio
import time
from pydub import AudioSegment
from pydub.playback import play
import win32ui
import pygame


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
        cv2.waitKey(1)
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

                    if loc == 'realm/novice': 
                        print(f"[DEBUG] Matches {len(matches)}")

                    if len(matches) > areas[loc].threshold:
                        print(f"[MATCH] Object matches with {len(matches)} for loc {loc}")
                        print(f"Should Play {areas[loc].track}")
                        location = loc
                        matched_vis = orb.draw_matches(target_images[loc][ref], kp1, game_image, kp2, matches)
                        # cv2.imshow("ORB Match", matched_vis)

            except Exception as e:
                print(f"[ERROR] {e}")
                print(target_images[loc][ref].shape)
                print(game_image.shape)

            if location:
                break
                
                
    return location

class Crossfader:
    def __init__(self, areas, fade_duration=2500, steps=100):
        pygame.mixer.init()
        pygame.init()
        

        def try_process_sound(track_path):
            try: 
                return pygame.mixer.Sound(track_path)
            except Exception as e:
                return None
            
        self.location_to_track_paths = {location : os.path.join(REF_DIR, location, areas[location].track) for location in areas}
        self.location_to_songs = {location : try_process_sound(track_path) for location, track_path in self.location_to_track_paths.items()}

        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)

        self.song1 = None
        self.song2 = None
        self.fade_duration = fade_duration
        self.steps = steps

    def crossfade(self, location: str):
        if self.song1 is None:
            print("No first track to crossfade from.")
            try:
                self.song1 = self.location_to_songs[location]

                self.channel1.set_volume(1.0)
                self.channel1.play(self.song1)
                print(f"Playing track: {self.track_paths[location]} ({location}) on channel1")
            except Exception as e:
                [print(f"error {e}: track_path: {self.track_paths[location]} ({location})") for i in range(20)]
            finally:
                return
        else:
            try:
                self.song2 = self.location_to_songs[location]
                self.channel2.set_volume(0.0)
                self.channel2.play(self.song2)
                step_delay = self.fade_duration / self.steps / 1000.0  # seconds

                # Gradually reduce volume on channel1 and increase on channel2.
                for i in range(self.steps):
                    vol1 = 1.0 - (i / self.steps)
                    vol2 = i / self.steps
                    self.channel1.set_volume(vol1)
                    self.channel2.set_volume(vol2)
                    time.sleep(step_delay)

                # Stop channel1 after crossfade.
                self.channel1.stop()
                print("Crossfade complete.")
                
                # Swap channels: channel2 (new track) becomes the primary channel.
                self.channel1, self.channel2 = self.channel2, self.channel1

                # Update song1 to be the new current track, and clear song2.
                self.song1 = self.song2
                self.song2 = None
            except Exception as e:
                [print(f"error {e}: track_path: {self.track_paths[location]} ({location})") for i in range(20)]
            finally:
                return

RUN = 'PROD'

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

    location = None
    last_location = None
    state = 'nexus'
    

    # Get all track filepaths and cache
    areas = Areas().update(REF_DIR)

    # Create empty results list for each area
    results = create_results_empty(areas)

    # Intialize playback and crossfader object with list of all tracks to load
    crossfader = Crossfader(areas)
    time.sleep(1)

    # Load all images into memory. This saves time to do it beforehand rather than repeatedly open the image file. 
    target_images, target_features = load_images_and_features(REF_DIR, orb, areas)




    for i in range(10000):
        try:
            game_image = window.capture_as_image()
            if RUN == 'DEBUG':
                cv2.imwrite(f'dataset/{i}.png', np.array(game_image))

            average_rgb = np.array(cv2.mean(np.array(game_image))[:3])  # returns (H, S, V, A) — we drop A
            results['colors'].append(average_rgb)
        except win32ui.error or findwindows.ElementAmbiguousError or findwindows.ElementNotFoundError as e:
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
        print(f"Track: {areas[location].track}")
        
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