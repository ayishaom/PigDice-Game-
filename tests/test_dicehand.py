"""Unit tests for DiceHand: construction, rolling, sum, any 1, double ones."""

import os
import sys
import unittest
from unittest.mock import patch

# Make src folder visible to import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from diceHand import DiceHand
from dice import Dice

# robust target for patching randint from Dice module
_DICE_MODULE = sys.modules[Dice.__module__]
_RANDINT_PATH = f"{_DICE_MODULE.__name__}.random.randint"


class TestDiceHand(unittest.TestCase):
    """Covers DiceHand: initialization, rolling, totals, flags."""

    def setUp(self):
        """Create a hand of two 6-sided dice."""
        self.hand = DiceHand(num_dice=2, sides=6)

    def test_default_hand_length(self):
        self.assertEqual(len(self.hand), 2)

    def test_roll_returns_values_and_updates_state(self):
        values = self.hand.roll()
        self.assertEqual(values, self.hand.values)
        for v in values:
            self.assertGreaterEqual(v, 1)
            self.assertLessEqual(v, 6)

    @patch(_RANDINT_PATH, side_effect=[1, 4])
    def test_roll_with_mock(self, mock_randint):
        values = self.hand.roll()
        self.assertEqual(values, [1, 4])
        self.assertEqual(self.hand.values, [1, 4])
        self.assertEqual(mock_randint.call_count, 2)
        for call in mock_randint.call_args_list:
            self.assertEqual(call.args, (1, 6))

    def test_total_returns_sum_of_values(self):
        with patch(_RANDINT_PATH, side_effect=[3, 5]):
            self.hand.roll()
        self.assertEqual(self.hand.total(), 8)

    def test_any_one_flag(self):
        with patch(_RANDINT_PATH, side_effect=[1, 4]):
            self.hand.roll()
        self.assertTrue(self.hand.any_one())

        with patch(_RANDINT_PATH, side_effect=[2, 3]):
            self.hand.roll()
        self.assertFalse(self.hand.any_one())

    def test_double_ones_flag(self):
        with patch(_RANDINT_PATH, side_effect=[1, 1]):
            self.hand.roll()
        self.assertTrue(self.hand.double_ones())

        with patch(_RANDINT_PATH, side_effect=[1, 3]):
            self.hand.roll()
        self.assertFalse(self.hand.double_ones())

    def test_init_invalid_num_dice_raises(self):
        with self.assertRaises(ValueError):
            DiceHand(num_dice=0)

    def test_len_returns_number_of_dice(self):
        self.assertEqual(len(self.hand), 2)

    def test_repr_returns_string(self):
        self.hand.values = [2, 5]
        self.assertEqual(repr(self.hand), "DiceHand([2, 5])")


if __name__ == "__main__":
    unittest.main()
