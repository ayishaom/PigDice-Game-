"""Unit tests for Player: construction, name changes, and score operations."""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from player import Player


class TestPlayer(unittest.TestCase):
    """Covers init, name/score setters, add/reset, invariants, and instance isolation."""

    # --- Construction ------------------------------------------------------

    def test_default_init_human(self):
        p = Player("Ana")
        self.assertEqual(p.get_name(), "Ana")
        self.assertFalse(p.is_ai)
        self.assertEqual(p.get_score(), 0)

    def test_init_ai_true(self):
        p = Player("Bot", is_ai=True)
        self.assertEqual(p.get_name(), "Bot")
        self.assertTrue(p.is_ai)
        self.assertEqual(p.get_score(), 0)

    def test_init_invalid_name_types_raise(self):
        for bad in ("", " ", None, 123, [], {}, 3.14):
            with self.assertRaises(ValueError):
                Player(bad)

    # --- Naming ------------------------------------------------------------

    def test_get_set_name_valid(self):
        p = Player("Ana")
        p.set_name("New Name")
        self.assertEqual(p.get_name(), "New Name")
        p.set_name("Zed")
        self.assertEqual(p.get_name(), "Zed")

    def test_set_name_invalid_preserves_previous_name(self):
        p = Player("Start")
        before = p.get_name()
        for bad in ("", " ", None, 0, [], {}, 1.5):
            with self.assertRaises(ValueError):
                p.set_name(bad)
            self.assertEqual(p.get_name(), before)

    # --- Scoring -----------------------------------------------------------

    def test_get_set_score_valid(self):
        p = Player("Ana")
        for val in (0, 15, 123456):
            p.set_score(val)
            self.assertEqual(p.get_score(), val)

    def test_set_score_invalid_preserves_previous_score(self):
        p = Player("Ana")
        p.set_score(7)
        before = p.get_score()
        for bad in (-1, -100, 3.5, "10", None, [], {}):
            with self.assertRaises(ValueError):
                p.set_score(bad)
            self.assertEqual(p.get_score(), before)

    def test_add_score_accumulates(self):
        p = Player("Ana")
        for add, expect in ((3, 3), (7, 10), (0, 10), (13, 23)):
            p.add_score(add)
            self.assertEqual(p.get_score(), expect)

    def test_add_score_invalid_preserves_score(self):
        p = Player("Ana")
        p.set_score(5)
        before = p.get_score()
        for bad in (-1, -10, "5", 2.2, None, [], {}):
            with self.assertRaises(ValueError):
                p.add_score(bad)
            self.assertEqual(p.get_score(), before)

    def test_reset_score_sets_zero_after_activity(self):
        p = Player("Ana")
        p.add_score(12)
        self.assertEqual(p.get_score(), 12)
        p.reset_score()
        self.assertEqual(p.get_score(), 0)

    # --- Instance isolation ------------------------------------------------

    def test_multiple_players_independent_state(self):
        a = Player("Ana")
        b = Player("Ben", is_ai=True)
        a.add_score(5)
        b.add_score(9)
        self.assertEqual(a.get_name(), "Ana")
        self.assertEqual(b.get_name(), "Ben")
        self.assertFalse(a.is_ai)
        self.assertTrue(b.is_ai)
        self.assertEqual(a.get_score(), 5)
        self.assertEqual(b.get_score(), 9)
        # Mutate A only; B must be unchanged
        a.set_name("AnaMaria")
        a.add_score(1)
        self.assertEqual(a.get_name(), "AnaMaria")
        self.assertEqual(a.get_score(), 6)
        self.assertEqual(b.get_name(), "Ben")
        self.assertEqual(b.get_score(), 9)


if __name__ == "__main__":
    unittest.main()
