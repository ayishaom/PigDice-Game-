import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from dice import Dice

class TestDice(unittest.TestCase):
    def test_roll_returns_value_in_range(self):
        """Test that roll() returns an integer between 1 and 6."""
        die = Dice()
        value = die.roll()
        self.assertIsInstance(value, int)
        self.assertGreaterEqual(value, 1)
        self.assertLessEqual(value, die.sides)

if __name__ == "__main__":
    unittest.main()