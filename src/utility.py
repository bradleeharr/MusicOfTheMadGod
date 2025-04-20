import os
import pygame
import cv2

def find_audio_files(directory):
    audio_files = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(('.mp3', '.wav', '.ogg', '.flac', '.aac')):
                file_path = os.path.join(root, file_name)
                audio_files.append(file_path)
    return audio_files

def try_process_sound(track_path, volume = 1.0):
    try: 
        s = pygame.mixer.Sound(track_path)
        s.set_volume(volume)
        return pygame.mixer.Sound(track_path)
    except Exception as e:
        print(f"[ERROR] {e}")
        return None
    
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
        cv2.waitKey(1)
        cv2.destroyAllWindows()


    return image[y1:y1+ch, x1:x1+ch]

def create_results_empty(areas):
    results = {}
    for loc in areas.keys():
        results['colors'] = []
        results[loc] = {
            'matches' : [],
        }
    return results


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