import os

class Area:
    def __init__(self, 
                 track: str = '',
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
            # -=-=-=-=-=-=-=-=- Nexus -=-=-=-=-=-=-=-=-
            'nexus/nexus' :          Area('', 90),
            'nexus/vault' :          Area('', 90),
            'nexus/queue' :         Area('',90),

            # -=-=-=-=-=-=-=-=- Realm -=-=-=-=-=-=-=-=-
            #'realm/coral-reefs' :    Area('z, 70),
            'realm/sprite-forest' :  Area(),
            'realm/deep-sea-abyss' : Area(),
            'realm/novice' :         Area(threshold=71),
            'realm/dead-church' :    Area(),
            'realm/runic-tundra':    Area(),
            'realm/floral-escape':    Area(),
            'realm/haunted-hallows': Area(),
            'realm/carboniferous' : Area(),
            'realm/coral-reefs' : Area(),
            'realm/sanguine-forest' : Area(),
            'realm/shipwreck-cove': Area(upper_rgb=(55, 55, 55), lower_rgb=(40,45,40)),

            # -=-=-=-=-=-=-=-=- Dungeons -=-=-=-=-=-=-=-=-
            'dungeon/sprite-world':  Area('', 99),
            'dungeon/moonlight-village': Area('', 80),
            'dungeon/magic-woods': Area('',100),
            'dungeon/fungal-cavern': Area('',90),
            'dungeon/puppet-masters-theatre': Area('',130),
            'dungeon/the-nest' : Area('',110),
            'dungeon/fungal-cavern' : Area('',110),
            'dungeon/crystal-cavern' : Area('', 110),
            'dungeon/sulfurous-wetlands' : Area('',110),
            'dungeon/abyss-of-demons' : Area('',110),
            'dungeon/tomb-of-the-ancients': Area('',120),
            'dungeon/toxic-sewers': Area('',110),
            'dungeon/ancient-ruins': Area('',110),
            'dungeon/parasite-chambers': Area('',110),
            'dungeon/deadwater-docks': Area('',110),
            'dungeon/woodland-labyrinth': Area('',110),


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