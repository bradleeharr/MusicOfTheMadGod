import pygame
import time
import random

import utility as utility

from utility import SoundAndVol

class Crossfader:
    def __init__(self, areas_dict, fade_duration=2500, steps=100):
        pygame.mixer.init()
        pygame.init()

        #     
        self.location_to_songs_and_vols = self.generate_location_to_songs_and_vols(areas_dict)
         
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)

        self.song1 = None
        self.song2 = None

        self.volume1 = 1.0
        self.volume2 = 1.0

        self.fade_duration = fade_duration
        self.steps = steps


    def generate_location_to_songs_and_vols(self, areas_dict):
        location_to_songs_and_vols = {}
    
        for location in areas_dict:
            for idx, track in enumerate(areas_dict[location].tracks):
                track_fp = track
                vol = areas_dict[location].volume

                if location not in location_to_songs_and_vols:
                    location_to_songs_and_vols[location] = []
                location_to_songs_and_vols[location].append(SoundAndVol(utility.try_process_sound(track_fp, vol), vol))
        return location_to_songs_and_vols
    

    def crossfade_first_track(self, sound_and_vol, location=""):
        try:
            self.song1 = sound_and_vol.sound
            self.volume1 = sound_and_vol.vol
            self.channel1.set_volume(self.volume1)
            self.channel1.play(self.song1)
            print(f"Playing track: {self.location_to_songs_and_vols[location]} ({location}) on channel1")
        except Exception as e:
            [print(f"error {e}: track_path: {self.location_to_songs_and_vols[location]} ({location})") for i in range(20)]
        finally:
            return

    def crossfade_second_track(self, sound_and_vol):
        self.song2 = sound_and_vol.sound
        self.volume2 = sound_and_vol.vol
        
        self.channel2.set_volume(0.0)
        self.channel2.play(self.song2)
        step_delay = self.fade_duration / self.steps / 1000.0  # seconds

        # Gradually reduce volume on channel1 and increase on channel2.
        for i in range(self.steps):
            vol1 = self.volume1 * (1.0 - (i / self.steps))
            vol2 = self.volume2 * (i / self.steps)
            self.channel1.set_volume(vol1)
            self.channel2.set_volume(vol2)
            time.sleep(step_delay)

        # Stop channel1 after crossfade.
        self.channel1.stop()
        print("Crossfade complete.")
        
        # Swap channels: channel2 (new track) becomes the primary channel.
        self.channel1, self.channel2 = self.channel2, self.channel1
        # Update song1 to be the new current track
        self.song1 = self.song2
        self.volume1 = self.volume2
        # clear song2.
        self.song2 = None
        self.volume2 = None


    def crossfade(self, location: str):
        if location not in self.location_to_songs_and_vols:
            print(f"[ERROR] Location not in songs_and_vols")
            return
        
        sound_and_vol = random.choice(self.location_to_songs_and_vols[location])        
        if self.song1 is None:
            print("No first track to crossfade from.")
            self.crossfade_first_track(sound_and_vol, location)
        else:
            try:
                self.crossfade_second_track(sound_and_vol)
            except Exception as e:
                [print(f"error {e}: track_path: {self.location_to_songs_and_vols[location]} ({location})") for i in range(20)]
            finally:
                return
