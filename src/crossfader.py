import pygame
import time
import random

import utility as utility

class Crossfader:
    def __init__(self, areas, fade_duration=2500, steps=100):
        pygame.mixer.init()
        pygame.init()
            
        self.location_to_songs_and_vols = {}
    
        for location in areas:
            for idx, track in enumerate(areas[location].tracks):
                track_fp = track
                vol = areas[location].volume

                class SoundAndVol:
                    def __init__(self, sound, vol):
                        self.sound = sound
                        self.vol = vol

                if location not in self.location_to_songs_and_vols:
                    self.location_to_songs_and_vols[location] = []
                self.location_to_songs_and_vols[location].append(SoundAndVol(utility.try_process_sound(track_fp, vol), vol))

        self.location_to_volumes = {location : areas[location].volume for location in areas}
         
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)

        self.song1 = None
        self.song2 = None

        self.volume1 = 1.0
        self.volume2 = 1.0

        self.fade_duration = fade_duration
        self.steps = steps

    def replay(self):
        if self.song1 is None:
            return
        else:
            self.channel1.play(self.song1)

    def crossfade(self, location: str):
        if location not in self.location_to_songs_and_vols:
            print(f"[ERROR] Location not in songs_and_vols")
            return
        
        sound_and_vol = random.choice(self.location_to_songs_and_vols[location])        
        if self.song1 is None:
            print("No first track to crossfade from.")
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
        else:
            try:
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

            except Exception as e:
                [print(f"error {e}: track_path: {self.location_to_songs_and_vols[location]} ({location})") for i in range(20)]
            finally:
                return
