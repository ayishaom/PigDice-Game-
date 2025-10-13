"""Unit tests for Dice: consctruction, rolling, side changes."""

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from dice import Dice
from unittest.mock import patch

# robust target for patching randint from the actual Dice modul
_DICE_MODULE = sys.modules[Dice.__module__]
_RANDINT_PATH = f"{_DICE_MODULE.__name__}.random.randint"

class TestDice(unittest.TestCase):
    """Covers init, rolling behavior and side updates."""

    def setUp(self):
        """Create a default 6-sided die."""
        self.die = Dice()

    def test_default_init(self):
        self.assertEqual(self.die.get_sides(), 6)
        self.assertIsNone(self.die.get_current_value())

    def test_custom_init_valid_values(self):
        for sides in (2, 7, 20):
            d = Dice(sides)
            self.assertEqual(d.get_sides(), sides)
            self.assertIsNone(d.get_current_value())
    
    def test_init_invalid_values_raise(self):
        invalid = [0, 1, -5, "6", 3.14, None]
        for bad in invalid:
            with self.assertRaises(ValueError):
                Dice(bad)

    def test_get_current_value_before_any_roll_is_none(self):
        self.assertIsNone(self.die.get_current_value())

    def test_roll_returns_in_range_and_updates_state(self):
        for _ in range(100):
            val = self.die.roll()
            self.assertGreaterEqual(val, 1)
            self.assertLessEqual(val, self.die.get_sides())
            self.assertEqual(self.die.get_current_value(), val)

    @patch(_RANDINT_PATH, return_value = 4)
    def test_roll_is_deterministic_with_mock(self, mock_randint):
        """Mocked randint -> fixed roll and correct bounds call."""
        val = self.die.roll()
        self.assertEqual(val, 4)
        self.assertEqual(self.die.get_current_value(), 4)
        mock_randint.assert_called_once_with(1, 6)

    def test_set_sides_valid_values(self):
        for sides in (8, 12, 24):
            self.die.set_sides(sides)
            self.assertEqual(self.die.get_sides(), sides)
            self.assertIsNone(self.die.get_current_value())

    def test_set_sides_invalid_preserves_previous_state(self):
        self.die.roll()
        previous_value = self.die.get_current_value()
        previous_sides = self.die.get_sides()

        for bad in (0, 1, -1, "a", 2.7, None):
            with self.assertRaises(ValueError):
                self.die.set_sides(bad)
            self.assertEqual(self.die.get_sides(), previous_sides)
            self.assertEqual(self.die.get_current_value(), previous_value)

    @patch(_RANDINT_PATH, side_effect = [1, 10])
    def test_roll_respects_new_sides_after_change(self, mock_randint):
        """After chaning sides, rolls use the new [1, sides] bounds."""
        self.die.set_sides(10)
        first = self.die.roll()
        self.assertEqual(first, 1)
        self.assertEqual(self.die.get_current_value(), 1)
        second = self.die.roll()
        self.assertEqual(second, 10)
        self.assertEqual(self.die.get_current_value(), 10)
        self.assertEqual(mock_randint.call_count, 2)
        for call in mock_randint.call_args_list:
            self.assertEqual(call.args, (1, 10))

    @patch(_RANDINT_PATH, return_value = 3)
    def test_random_called_with_correct_bounds_default(self, mock_randint):
        self.die.roll()
        mock_randint.assert_called_once_with(1, 6)

    def test_multiple_dice_instances_have_dependent_state(self):
        a = Dice(6)
        b = Dice(6)
        with patch(_RANDINT_PATH, side_effect = [2, 5]) as mock_randint:
            va = a.roll()
            vb = b.roll()
        self.assertEqual(va, 2)
        self.assertEqual(vb, 5)
        self.assertEqual(a.get_current_value(), 2)
        self.assertEqual(b.get_current_value(), 5)
        self.assertEqual(mock_randint.call_count, 2)

    def test_changing_sides_then_rolling_stays_within_new_bounds(self):
        self.die.set_sides(20)
        for _ in range(50):
            val = self.die.roll()
            self.assertGreaterEqual(val, 1)
            self.assertLessEqual(val, 20)

if __name__ == "__main__":
    unittest.main()