"""Unit tests for Dice: construction, rolling, side changes, and state."""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from dice import Dice

# Build a robust patch path to randint inside the actual dice module
_DICE_MODULE = sys.modules[Dice.__module__]
_RANDINT_PATH = f"{_DICE_MODULE.__name__}.random.randint"


class TestDice(unittest.TestCase):
    """Covers init, roll behavior, bounds, side updates, and instance isolation."""

    def setUp(self):
        self.die = Dice()

    # --- Construction ------------------------------------------------------

    def test_default_init(self):
        self.assertEqual(self.die.get_sides(), 6)
        self.assertIsNone(self.die.get_current_value())

    def test_custom_init_valid_values(self):
        for sides in (2, 7, 20):
            d = Dice(sides)
            self.assertEqual(d.get_sides(), sides)
            self.assertIsNone(d.get_current_value())

    def test_init_invalid_values_raise(self):
        for bad in (0, 1, -5, "6", 3.14, None):
            with self.assertRaises(ValueError):
                Dice(bad)

    # --- Rolling -----------------------------------------------------------

    def test_current_value_none_before_first_roll(self):
        self.assertIsNone(self.die.get_current_value())

    def test_roll_updates_state_and_stays_in_bounds(self):
        for _ in range(12):
            val = self.die.roll()
            self.assertGreaterEqual(val, 1)
            self.assertLessEqual(val, self.die.get_sides())
            self.assertEqual(self.die.get_current_value(), val)

    @patch(_RANDINT_PATH, return_value=4)
    def test_roll_deterministic_with_mock(self, mock_randint):
        val = self.die.roll()
        self.assertEqual(val, 4)
        self.assertEqual(self.die.get_current_value(), 4)
        mock_randint.assert_called_once_with(1, 6)

    # --- Changing sides ----------------------------------------------------

    def test_set_sides_valid_updates_bounds_and_preserves_value(self):
        with patch(_RANDINT_PATH, return_value=3):
            self.assertEqual(self.die.roll(), 3)
        self.assertEqual(self.die.get_current_value(), 3)
        self.die.set_sides(10)
        self.assertEqual(self.die.get_sides(), 10)
        self.assertEqual(self.die.get_current_value(), 3)

    def test_set_sides_invalid_preserves_previous_state(self):
        with patch(_RANDINT_PATH, return_value=5):
            self.assertEqual(self.die.roll(), 5)
        prev_val = self.die.get_current_value()
        prev_sides = self.die.get_sides()
        for bad in (0, 1, -1, "a", 2.7, None):
            with self.assertRaises(ValueError):
                self.die.set_sides(bad)
            self.assertEqual(self.die.get_sides(), prev_sides)
            self.assertEqual(self.die.get_current_value(), prev_val)

    @patch(_RANDINT_PATH, side_effect=[1, 10])
    def test_roll_uses_new_bounds_after_side_change(self, mock_randint):
        self.die.set_sides(10)
        first = self.die.roll()
        second = self.die.roll()
        self.assertEqual(first, 1)
        self.assertEqual(second, 10)
        self.assertEqual(self.die.get_current_value(), 10)
        self.assertEqual(mock_randint.call_count, 2)
        for call in mock_randint.call_args_list:
            self.assertEqual(call.args, (1, 10))

    # --- Instance isolation & dunder basics --------------------------------

    def test_multiple_dice_instances_are_independent(self):
        a = Dice(6)
        b = Dice(6)
        with patch(_RANDINT_PATH, side_effect=[2, 5]):
            va = a.roll()
            vb = b.roll()
        self.assertEqual(va, 2)
        self.assertEqual(vb, 5)
        self.assertEqual(a.get_current_value(), 2)
        self.assertEqual(b.get_current_value(), 5)

    def test_len_and_repr_behave_reasonably(self):
        self.assertIsInstance(repr(self.die), str)
        with patch(_RANDINT_PATH, return_value=6):
            self.die.roll()
        self.assertIn("Dice", repr(self.die))

    def test_random_called_with_correct_bounds_default(self):
        with patch(_RANDINT_PATH, return_value=2) as mock_randint:
            self.die.roll()
        mock_randint.assert_called_once_with(1, 6)


if __name__ == "__main__":
    unittest.main()
