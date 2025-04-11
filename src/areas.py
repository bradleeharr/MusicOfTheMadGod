import os
import numpy as np

class Area:
    def __init__(self, 
                 track: str = '',
                 threshold: float = 999, 
                 volume: int = 0.8, 
                 average_color = (0,0,0),
                 upper_rgb = (0,0,0),
                 lower_rgb = (0,0,0)
                 ):
        self.track = track
        self.threshold = threshold
        self.volume = volume
        self.average_color = average_color
        self.upper_rgb = np.array(upper_rgb)
        self.lower_rgb = np.array(lower_rgb)
    def __repr__(self):
        return f"Track: {self.track}|Threshold: {self.threshold}|Volume: {self.volume}\n"

class Areas:
    def __init__(self):
        self.dict = {
            # -=-=-=-=-=-=-=-=- Nexus -=-=-=-=-=-=-=-=-
            'nexus/daily-quest-room' :           Area(threshold=96, volume=0.8),
            'nexus/nexus' :                      Area(threshold=90, volume=0.8),
            'nexus/vault' :                      Area(threshold=90, volume=1.4),
            'nexus/queue' :                      Area(threshold=90, 
                                                      upper_rgb=[48, 56, 48], lower_rgb=[45, 53, 45],
                                                      volume=0.5),
            'nexus/pet-yard' :                   Area(threshold=100),
            # -=-=-=-=-=-=-=-=- Realm -=-=-=-=-=-=-=-=-
            'realm/sprite-forest' :              Area(upper_rgb=[68, 70, 95],    lower_rgb=[55, 64, 80]),
            'realm/deep-sea-abyss' :             Area(upper_rgb=[64, 70, 75],    lower_rgb=[55, 60, 60]),
            'realm/novice' :                     Area(threshold=75,
                                                    volume=0.8),
            'realm/dead-church' :                Area(upper_rgb=[68, 55, 32],    lower_rgb=[58, 45, 25]),
            'realm/runic-tundra':                Area(upper_rgb=[100, 120, 130], lower_rgb=[80, 100, 110]),
            'realm/floral-escape':               Area(upper_rgb=[95, 110, 50],   lower_rgb=[80, 90, 40]),
            'realm/haunted-hallows':             Area(upper_rgb=[40, 40, 58],    lower_rgb=[30, 30, 50],
                                                    volume=0.25),
            'realm/carboniferous' :              Area(upper_rgb=[80, 83, 65],    lower_rgb=[65, 73, 55]),
            'realm/coral-reefs' :                Area(upper_rgb=[150, 130, 118], lower_rgb=[140, 115, 100], volume=0.5),
            'realm/shipwreck-cove':              Area(upper_rgb=(55, 55, 55),    lower_rgb=[40,45,40],
                                                    volume=0.6),
            'realm/sanguine-forest' :            Area(upper_rgb=[52, 30, 35],    lower_rgb=[41, 19, 25]),
            'realm/risen-hell' :                 Area(upper_rgb=[60, 40, 40], lower_rgb=[50, 30, 30]), 
            'realm/abandoned-city' :             Area(upper_rgb=[105, 85, 85], lower_rgb=[95, 75, 75]),
            # -=-=-=-=-=-=-=-=- Dungeons -=-=-=-=-=-=-=-=-
            'dungeon/sprite-world':              Area(threshold=99),
            'dungeon/moonlight-village':         Area(threshold=110, volume=0.25),
            'dungeon/magic-woods':               Area(threshold=100),
            'dungeon/fungal-cavern':             Area(threshold=90),
            'dungeon/puppet-masters-theatre':    Area(threshold=130),
            'dungeon/puppet-masters-encore':     Area(threshold=130, volume=0.4),
            'dungeon/the-nest' :                 Area(threshold=110, volume=0.25),
            'dungeon/fungal-cavern' :            Area(threshold=110),
            'dungeon/crystal-cavern' :           Area(threshold=105),
            'dungeon/sulfurous-wetlands' :       Area(threshold=110),
            'dungeon/abyss-of-demons' :          Area(threshold=110),
            'dungeon/tomb-of-the-ancients':      Area(threshold=99),
            'dungeon/toxic-sewers':              Area(threshold=110),
            'dungeon/ancient-ruins':             Area(threshold=100),
            'dungeon/parasite-chambers':         Area(threshold=110),
            'dungeon/deadwater-docks':           Area(threshold=110, volume=0.8),
            'dungeon/woodland-labyrinth':        Area(threshold=110),
            'dungeon/the-third-dimension':       Area(threshold=110),
            'dungeon/high-tech-terror':          Area(threshold=110),
            'dungeon/cultist-hideout':           Area(threshold=110),
            'dungeon/the-void' :                 Area(threshold=110),
            'dungeon/lost-halls' :               Area(threshold=110),
            'dungeon/davy-jones-locker':         Area(threshold=98),
            'dungeon/mad-lab' :                  Area(threshold=110),
            'dungeon/undead-lair' :              Area(threshold=110),
            'dungeon/lair-of-draconis':          Area(threshold=110),
            'dungeon/lair-of-shaitan':           Area(threshold=110),
            'dungeon/candyland-hunting-grounds': Area(threshold=110),
            'dungeon/ice-cave':                  Area(threshold=110),

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