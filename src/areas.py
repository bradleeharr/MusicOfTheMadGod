import os
import numpy as np

import utility as utility
import config as config

class Areas:
    def __init__(self):
        self.dict = config.dict

    def update(self, ref_dir):
        # Get all track filepaths and cache
        for loc in self.dict.keys():
            dir = os.path.join(ref_dir, loc)
            if not os.path.exists(dir):
                continue
            self.dict[loc].tracks = utility.find_audio_files(dir)
            if not self.dict[loc].tracks:
                print(f"[ERROR] NO AUDIO FILES FOUND! loc - {loc} / dir - {dir}")
                continue
            print(f"[DEBUG] Set Area {loc} Tracks to {self.dict[loc].tracks}")
        print(self.dict)
        return self.dict