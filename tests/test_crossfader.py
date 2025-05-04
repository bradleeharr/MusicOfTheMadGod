from crossfader import Crossfader
from areas import Areas

from unittest.mock import Mock


def test_crossfader_generate_location_to_songs_and_vols():
    mock_areas = Mock()
    mock_areas.dict = {}
    

    crossfader = Crossfader(mock_areas.dict)

    crossfader.generate_location_to_songs_and_vols(mock_areas.dict)

def test_crossfader_init():
    mock_areas = Mock()
    mock_areas.dict = {}
    
    crossfader = Crossfader(mock_areas.dict)

def test_replay():
    mock_areas = Mock()
    mock_areas.dict = {}

    crossfader = Crossfader(mock_areas.dict)
    crossfader.replay()

def test_crossfade_empty():
    mock_areas = Mock()
    mock_areas.dict = {}

    crossfader = Crossfader(mock_areas.dict)
    crossfader.replay()
    crossfader.crossfade("")
    crossfader.crossfade("")
    crossfader.crossfade("")
