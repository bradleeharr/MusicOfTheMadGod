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

def try_process_sound(track_path, volume):
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
