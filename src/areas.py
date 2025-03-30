import os

class Area:
    def __init__(self, 
                 track: str,
                 threshold: float = 999, 
                 volume: int = 50, 
                 average_color = (0,0,0),
                 upper_rgb = (0,0,0),
                 lower_rgb = (0,0,0)
                 ):
        self.track = track
        self.threshold = threshold
        self.volume = volume
        self.average_color = average_color
        self.upper_rgb = upper_rgb
        self.lower_rgb = lower_rgb
    def __repr__(self):
        return f"Track: {self.track}|Threshold: {self.threshold}|Volume: {self.volume}\n"

class Areas:
    def __init__(self):
        self.dict = {
            'nexus/nexus' :          Area('', 80),
            'nexus/vault' :          Area('', 90),
            'nexus/queue' :         Area('',90),
            #'realm/coral-reefs' :    Area('', 70),
            'realm/sprite-forest' :  Area('', 75),
            'realm/deep-sea-abyss' : Area('', 30),
            'realm/novice' :         Area('', 70),
            'realm/dead-church' :    Area('', 75),
            'realm/runic-tundra':    Area('', 50),
            'realm/floral-escape':    Area('', 50),
            'realm/haunted-hallows': Area('', 50),
            'realm/carboniferous' : Area(''),
            'dungeon/sprite-world':  Area('', 99),
            'dungeon/moonlight-village': Area('', 80),
            'dungeon/magic-woods': Area('', 80),
            'dungeon/fungal-cavern': Area('',90),

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