import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

"""Unit tests for Player: construction, name changes and score operations."""

import unittest
from player import Player

class TestPlayer(unittest.TestCase):
    """Covers init, name/score setters, add/reset and invariants."""

    def test_default_init_human(self):
        """Human player starts with given name, is_ai False and score 0."""
        p = Player("Ana")
        self.assertEqual(p.get_name(), "Ana")
        self.assertFalse(p.is_ai)
        self.assertEqual(p.get_score(), 0)

    def test_init_ai_true(self):
        """AI player is stored correctly, score starts at 0."""
        p =Player("Bot", is_ai=True)
        self.assertEqual(p.get_name(), "Bot")
        self.assertTrue(p.is_ai)
        self.assertEqual(p.get_score(), 0)

    def test_init_invalid_name_types_raise(self):
        """Invalid names (type/empty) raises ValueError."""
        invalid = ["", " ", None, 123, [], {}, 3.14]
        for bad in invalid:
            with self.assertRaises(ValueError):
                Player(bad)
    
    def test_get_set_name_valid(self):
        """Setting a valid new name updates the stored name."""
        p = Player("Ana")
        p.set_name("New Name")
        self.assertEqual(p.get_name(), "New Name")
        # change again to ensure repeated success
        p.set_name("Zed")
        self.assertEqual(p.get_name(), "Zed")

    def test_set_name_invalid_preserves_previous_name(self):
        """Invalid names raise and do not change the current name."""
        p = Player("Start")
        previous = p.get_name()
        for bad in ["", " ", None, 0, [], {}, 1.5]:
            with self.assertRaises(ValueError):
                p.set_name(bad)
            self.assertEqual(p.get_name(), previous)

    def test_get_set_score_valid(self):
        """Setting a non-negative integer score updates total_score."""
        p = Player("Ana")
        p.set_score(15)
        self.assertEqual(p.get_score(), 15)
        p.set_score(0)
        self.assertEqual(p.get_score(), 0)
        p.set_score(123456)
        self.assertEqual(p.get_score(), 123456)

    def test_set_score_invalid_preserves_previous_score(self):
        """Invalid scores raise and do not change stored score."""
        p = Player("Ana")
        p.set_score(7)
        previous = p.get_score()
        for bad in [-1, -100, 3.5, "10", None, [], {}]:
            with self.assertRaises(ValueError):
                p.set_score(bad)
            self.assertEqual(p.get_score(), previous)

    def test_add_score_accumulates(self):
        """Adding non-negative ints accumulates to total_score."""
        p = Player("Ana")
        p.add_score(3)
        self.assertEqual(p.get_score(), 3)
        p.add_score(7)
        self.assertEqual(p.get_score(), 10)
        p.add_score(0)
        self.assertEqual(p.get_score(), 10)
        p.add_score(13)
        self.assertEqual(p.get_score(), 23)

    def test_add_score_invalid_preserves_score(self):
        """Invalid points for add_score raise and keep previous score."""
        p = Player("Ana")
        p.set_score(5)
        previous = p.get_score()
        for bad in [-1, -10, "5", 2.2, None, [], {}]:
            with self.assertRaises(ValueError):
                p.add_score(bad)
            self.assertEqual(p.get_score(), previous)

    def test_reset_score_sets_zero(self):
        """reset_score() sets total_score to zero."""
        p = Player("Ana")
        p.add_score(12)
        self.assertEqual(p.get_score(), 12)
        p.reset_score()
        self.assertEqual(p.get_score(), 0)

    def test_multiple_players_independent_state(self):
        """Two players keep independent names, flags and scores."""
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
        # change one and ensure the other is unaffected
        a.set_name("AnaMaria")
        a.add_score(1)
        self.assertEqual(a.get_name(), "AnaMaria")
        self.assertEqual(a.get_score(), 6)
        self.assertEqual(b.get_name(), "Ben")
        self.assertEqual(b.get_score(), 9)

if __name__ == "__main__":
    unittest.main()
