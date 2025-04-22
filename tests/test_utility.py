import cv2
import os
from globals import REF_DIR

from utility import find_audio_files,  try_process_sound, crop_image, create_results_empty
 
test_loc = "nexus/nexus"

dir_path   = os.path.join(os.curdir, REF_DIR, test_loc)
image_path = os.path.join(dir_path, "image.png")
audio_path = os.path.join(dir_path, "test_audio.mp3")

def test_find_audio_files():
    files = find_audio_files(dir_path)
    assert audio_path in files 

    
def test_try_process_sound():
    valid = try_process_sound(audio_path, 1.0)
    assert valid is not None
    invalid = try_process_sound(audio_path+"notexistent", 1.0)
    assert invalid is None

def test_crop_image():
    img = cv2.imread(image_path)
    crop_image(img)