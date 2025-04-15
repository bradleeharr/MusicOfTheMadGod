import os
import pygame

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