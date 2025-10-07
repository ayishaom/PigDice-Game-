import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Dice import Dice

def test_dice_roll_returns_int():
    d = Dice()
    value = d.roll()
    assert isinstance(value, int)
    assert 1 <= value <= 6
