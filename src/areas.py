    
class Area:
    def __init__(self, track: str, threshold: float):
        self.track = track
        self.threshold = threshold


areas = {
    'nexus/nexus' :          Area('', 90),
    'nexus/vault' :          Area('', 70),
    'realm/coral-reefs' :    Area('', 70),
    'realm/sprite' :         Area('', 75),
    'realm/deep-sea-abyss' : Area('', 30),
    'realm/novice' :   Area('', 70),
    'realm/dead-church' : Area('', 75),
    
}