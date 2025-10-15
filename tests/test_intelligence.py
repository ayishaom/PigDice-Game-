"""Unit tests for Intelligence class: decision-making AI for Pig game."""

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from intelligence import Intelligence

class TestIntelligence(unittest.TestCase):
    """Covers AI decisions for easy, medium, and hard difficulties."""

    def setUp(self):
        """Create default AI (medium difficulty)."""
        self.ai = Intelligence()

    def test_default_init(self):
        self.assertEqual(self.ai.difficulty, "medium")
        self.assertEqual(self.ai.hold_threshold, 20)

    def test_set_difficulty_valid_levels(self):
        levels = {"easy": 15, "medium": 20, "hard": 25}
        for level, threshold in levels.items():
            self.ai.set_difficulty(level)
            self.assertEqual(self.ai.difficulty, level)
            self.assertEqual(self.ai.hold_threshold, threshold)

    def test_set_difficulty_invalid_raises(self):
        with self.assertRaises(ValueError):
            self.ai.set_difficulty("impossible")

    def test_decide_hold_if_reaches_100(self):
        self.assertEqual(self.ai.decide(turn_total=50, my_score=60, opponent_score=20), "hold")

    # --- Easy difficulty ---
    def test_easy_decision(self):
        self.ai.set_difficulty("easy")
        self.assertEqual(self.ai.decide(turn_total=16, my_score=10, opponent_score=10), "hold")
        self.assertEqual(self.ai.decide(turn_total=10, my_score=10, opponent_score=10), "roll")

    # --- Medium difficulty ---
    def test_medium_hold_threshold(self):
        self.ai.set_difficulty("medium")
        self.assertEqual(self.ai.decide(turn_total=20, my_score=50, opponent_score=50), "hold")

    def test_medium_opponent_close_to_winning(self):
        self.ai.set_difficulty("medium")
        self.assertEqual(self.ai.decide(turn_total=17, my_score=50, opponent_score=90), "roll")
        self.assertEqual(self.ai.decide(turn_total=18, my_score=50, opponent_score=90), "hold")

    # --- Hard difficulty ---
    def test_hard_decision_basic(self):
        self.ai.set_difficulty("hard")
        # Turn total below threshold
        self.assertEqual(self.ai.decide(turn_total=5, my_score=50, opponent_score=50), "roll")
        # Turn total above threshold
        self.assertEqual(self.ai.decide(turn_total=30, my_score=50, opponent_score=50), "hold")

    def test_hard_decision_score_gap_adjustment(self):
        self.ai.set_difficulty("hard")
        # AI behind opponent -> threshold slightly higher, so still roll
        self.assertEqual(self.ai.decide(turn_total=20, my_score=50, opponent_score=70), "roll")
        # AI far ahead -> threshold lower, might hold
        self.assertEqual(self.ai.decide(turn_total=20, my_score=70, opponent_score=50), "hold")

    def test_hard_decision_opponent_near_win(self):
        self.ai.set_difficulty("hard")
        self.assertEqual(self.ai.decide(turn_total=10, my_score=50, opponent_score=92), "hold")

if __name__ == "__main__":
    unittest.main()
