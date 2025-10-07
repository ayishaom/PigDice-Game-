import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Player import Player

def test_player_has_id_and_can_rename():
    p = Player("Ana")
    original_id = p.pid
    p.rename("Anastasia")
    assert p.pid == original_id
    assert p.name == "Anastasia"
    assert p.score == 0
