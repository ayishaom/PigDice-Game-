"""Unit tests for DiceHand: construction, rolling, total calculation,
and flags."""

import os
import sys
import unittest
from unittest.mock import patch

# Make src folder visible to import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', 'src')))

from diceHand import DiceHand
from dice import Dice


# Robust target for patching randint from Dice module
_DICE_MODULE = sys.modules[Dice.__module__]
_RANDINT_PATH = f"{_DICE_MODULE.__name__}.random.randint"


class TestDiceHand(unittest.TestCase):
    """Unit tests for the DiceHand class covering initialization, rolling,
    totals, and flags."""

    def setUp(self):
        """Set up a DiceHand instance with 2 six-sided dice for each test."""
        self.hand = DiceHand(num_dice=2, sides=6)

    def test_default_hand_length(self):
        """Test that the default number of dice in a hand is 2."""
        self.assertEqual(len(self.hand), 2)

    def test_roll_returns_values_and_updates_state(self):
        """Test that rolling updates values and all dice are within valid
        bounds."""
        values = self.hand.roll()
        self.assertEqual(values, self.hand.values)
        for v in values:
            self.assertGreaterEqual(v, 1)
            self.assertLessEqual(v, 6)

    @patch(_RANDINT_PATH, side_effect=[1, 4])
    def test_roll_with_mock(self, mock_randint):
        """Test rolling with mocked randint to produce predictable results."""
        values = self.hand.roll()
        self.assertEqual(values, [1, 4])
        self.assertEqual(self.hand.values, [1, 4])
        self.assertEqual(mock_randint.call_count, 2)
        for call in mock_randint.call_args_list:
            self.assertEqual(call.args, (1, 6))

    def test_total_returns_sum_of_values(self):
        """Test that the total method returns the sum of all dice values."""
        with patch(_RANDINT_PATH, side_effect=[3, 5]):
            self.hand.roll()
        self.assertEqual(self.hand.total(), 8)

    def test_any_one_flag(self):
        """Test that any_one() correctly identifies if a die rolled a 1."""
        with patch(_RANDINT_PATH, side_effect=[1, 4]):
            self.hand.roll()
        self.assertTrue(self.hand.any_one())

        with patch(_RANDINT_PATH, side_effect=[2, 3]):
            self.hand.roll()
        self.assertFalse(self.hand.any_one())

    def test_double_ones_flag(self):
        """Test that double_ones() correctly identifies two dice showing 1."""
        with patch(_RANDINT_PATH, side_effect=[1, 1]):
            self.hand.roll()
        self.assertTrue(self.hand.double_ones())

        with patch(_RANDINT_PATH, side_effect=[1, 3]):
            self.hand.roll()
        self.assertFalse(self.hand.double_ones())

    def test_init_invalid_num_dice_raises(self):
        """Test that initializing DiceHand with invalid number of dice raises
        ValueError."""
        with self.assertRaises(ValueError):
            DiceHand(num_dice=0)

    def test_len_returns_number_of_dice(self):
        """Test that len(DiceHand) returns the correct number of dice."""
        self.assertEqual(len(self.hand), 2)

    def test_repr_returns_string(self):
        """Test that repr(DiceHand) returns a string representation including
        dice values."""
        self.hand.values = [2, 5]
        self.assertEqual(repr(self.hand), "DiceHand([2, 5])")


if __name__ == "__main__":
    """Run the DiceHand unit tests."""
    unittest.main()
