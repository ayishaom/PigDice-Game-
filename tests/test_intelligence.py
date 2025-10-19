"""Unit tests for Intelligence class: verify AI decision-making
for Pig game."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', 'src')))

from intelligence import Intelligence


class TestIntelligence(unittest.TestCase):
    """Test AI decisions at easy, medium, and hard difficulty levels."""

    def setUp(self):
        """Create default AI instance with medium difficulty."""
        self.ai = Intelligence()

    # --- Initialization ---------------------------------------------------

    def test_default_init(self):
        """Initialize AI and confirm default difficulty and hold threshold."""
        self.assertEqual(self.ai.difficulty, "medium")
        self.assertEqual(self.ai.hold_threshold, 20)

    def test_set_difficulty_valid_levels(self):
        """Set AI difficulty to valid levels and confirm thresholds."""
        levels = {"easy": 15, "medium": 20, "hard": 25}
        for level, threshold in levels.items():
            self.ai.set_difficulty(level)
            self.assertEqual(self.ai.difficulty, level)
            self.assertEqual(self.ai.hold_threshold, threshold)

    def test_set_difficulty_invalid_raises(self):
        """Raise ValueError when setting invalid difficulty level."""
        with self.assertRaises(ValueError):
            self.ai.set_difficulty("impossible")

    # --- Decision-making ---------------------------------------------------

    def test_decide_hold_if_reaches_100(self):
        """Return 'hold' if AI would reach or exceed 100 points this turn."""
        self.assertEqual(self.ai.decide(
            turn_total=50, my_score=60, opponent_score=20), "hold")

    # --- Easy difficulty ---------------------------------------------------

    def test_easy_decision(self):
        """Decide whether to roll or hold on easy difficulty
        based on threshold."""
        self.ai.set_difficulty("easy")
        self.assertEqual(self.ai.decide(
            turn_total=16, my_score=10, opponent_score=10), "hold")
        self.assertEqual(self.ai.decide(
            turn_total=10, my_score=10, opponent_score=10), "roll")

    # --- Medium difficulty -------------------------------------------------

    def test_medium_hold_threshold(self):
        """Hold when turn total reaches medium difficulty threshold."""
        self.ai.set_difficulty("medium")
        self.assertEqual(self.ai.decide(
            turn_total=20, my_score=50, opponent_score=50), "hold")

    def test_medium_opponent_close_to_winning(self):
        """Adjust medium difficulty decisions when
        opponent is close to winning."""
        self.ai.set_difficulty("medium")
        self.assertEqual(self.ai.decide(
            turn_total=17, my_score=50, opponent_score=90), "roll")
        self.assertEqual(self.ai.decide(
            turn_total=18, my_score=50, opponent_score=90), "hold")

    # --- Hard difficulty ---------------------------------------------------

    def test_hard_decision_basic(self):
        """Decide whether to roll or hold on hard difficulty
        using threshold."""
        self.ai.set_difficulty("hard")
        self.assertEqual(self.ai.decide(
            turn_total=5, my_score=50, opponent_score=50), "roll")
        self.assertEqual(self.ai.decide(
            turn_total=30, my_score=50, opponent_score=50), "hold")

    def test_hard_decision_score_gap_adjustment(self):
        """Adjust hard difficulty decisions based on score
        difference with opponent."""
        self.ai.set_difficulty("hard")
        self.assertEqual(self.ai.decide(
            turn_total=20, my_score=50, opponent_score=70), "roll")
        self.assertEqual(self.ai.decide(
            turn_total=20, my_score=70, opponent_score=50), "hold")

    def test_hard_decision_opponent_near_win(self):
        """Hold on hard difficulty when opponent is close to winning."""
        self.ai.set_difficulty("hard")
        self.assertEqual(self.ai.decide(
            turn_total=10, my_score=50, opponent_score=92), "hold")


if __name__ == "__main__":
    unittest.main()
