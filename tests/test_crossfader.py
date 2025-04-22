from crossfader import Crossfader
from areas import Areas

from unittest.mock import Mock

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
