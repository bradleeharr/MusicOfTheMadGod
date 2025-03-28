    
class Area:
    def __init__(self, track: str, threshold: float, volume: int = 50):
        self.track = track
        self.threshold = threshold
        self.volume = volume


areas = {
    'nexus/nexus' :          Area('', 80),
    'nexus/vault' :          Area('', 80),
    'realm/coral-reefs' :    Area('', 70),
    'realm/sprite-forest' :         Area('', 75),
    'realm/deep-sea-abyss' : Area('', 30),
    'realm/novice' :   Area('', 70),
    'realm/dead-church' : Area('', 75),

    'dungeon/sprite-world': Area('', 99),
    
}