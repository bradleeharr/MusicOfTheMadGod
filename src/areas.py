import os

class Area:
    def __init__(self, track: str, threshold: float, volume: int = 50):
        self.track = track
        self.threshold = threshold
        self.volume = volume
    def __repr__(self):
        return f"Track: {self.track}|Threshold: {self.threshold}|Volume: {self.volume}\n"

class Areas:
    def __init__(self):
        self.dict = {
            'nexus/nexus' :          Area('', 80),
            'nexus/vault' :          Area('', 80),
            #'realm/coral-reefs' :    Area('', 70),
            'realm/sprite-forest' :  Area('', 75),
            #'realm/deep-sea-abyss' : Area('', 30),
            'realm/novice' :         Area('', 70),
            #'realm/dead-church' :    Area('', 75),
            'dungeon/sprite-world':  Area('', 99),
            
        }

    def update(self, ref_dir):
        # Get all track filepaths and cache
        for loc in self.dict.keys():
            dir = os.path.join(ref_dir, loc)
            for ref_file in os.listdir(dir):
                if not ref_file.lower().endswith((".mp3", ".wav", ".flac")):
                    continue
                self.dict[loc].track = ref_file
                print(f"[DEBUG] Set Area {loc} Track to {ref_file}")
        print(self.dict)
        return self.dict