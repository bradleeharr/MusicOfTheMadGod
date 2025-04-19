from utility import find_audio_files,  try_process_sound, crop_image, create_results_empty
 
def test_find_audio_files():
    find_audio_files("")

def test_try_process_sound():
    try_process_sound("", 1.0)

def test_crop_image():
    import cv2
    img = cv2.imread("ref/nexus/nexus/image.png")
    crop_image(img)