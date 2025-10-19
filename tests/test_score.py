"""Unit tests for Score: record games, retrieve scores, rename players,
clear scores, and handle file I/O."""

import os
import sys
import unittest
from unittest.mock import mock_open, patch
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..", "src")))

from score import Score


class TestScore(unittest.TestCase):
    """Test Score initialization, game recording, high-score retrieval,
    renaming, clearing, and edge cases."""

    def setUp(self):
        """Patch file and JSON operations; create Score instance without
        touching disk."""
        self.mock_open = mock_open()
        patcher = patch("builtins.open", self.mock_open)
        self.addCleanup(patcher.stop)
        self.mock_file = patcher.start()

        self.json_load_patcher = patch("json.load", return_value={})
        self.addCleanup(self.json_load_patcher.stop)
        self.mock_json_load = self.json_load_patcher.start()

        self.json_dump_patcher = patch("json.dump")
        self.addCleanup(self.json_dump_patcher.stop)
        self.mock_json_dump = self.json_dump_patcher.start()

        self.score = Score(file_path="dummy.json")

    # --- Initialization & load --------------------------------------------

    def test_initial_scores_empty_when_file_missing(self):
        """Initialize Score with nonexistent file and confirm
        empty dictionary."""
        self.mock_json_load.return_value = {}
        s = Score("nonexistent.json")
        self.assertEqual(s.scores, {})

    # --- record_game -------------------------------------------------------

    def test_record_game_creates_new_player(self):
        """Record points for a new player and verify scores and game list."""
        self.score.record_game("Lulu", 10)
        self.assertIn("Lulu", self.score.scores)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 10)
        self.assertEqual(len(self.score.scores["Lulu"]["games"]), 1)
        self.mock_json_dump.assert_called()

    def test_record_game_multiple_entries_updates_total(self):
        """Accumulate points for existing player and track multiple games."""
        self.score.record_game("Lulu", 10)
        self.score.record_game("Lulu", 5)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 15)
        self.assertEqual(len(self.score.scores["Lulu"]["games"]), 2)

    # --- get_high_scores ---------------------------------------------------

    def test_get_high_scores_sorted_descending(self):
        """Return players sorted by total points in descending order."""
        self.score.record_game("Lulu", 10)
        self.score.record_game("Anastasia", 15)
        top_scores = self.score.get_high_scores()
        self.assertEqual(top_scores[0][0], "Anastasia")
        self.assertEqual(top_scores[1][0], "Lulu")

    # --- get_player_history -----------------------------------------------

    def test_get_player_history_existing_player(self):
        """Retrieve full history for an existing player."""
        self.score.record_game("Lulu", 7)
        history = self.score.get_player_history("Lulu")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["points"], 7)

    def test_get_player_history_nonexistent_player(self):
        """Return empty list for a player not in the scores."""
        history = self.score.get_player_history("Nonexistent")
        self.assertEqual(history, [])

    # --- rename_player -----------------------------------------------------

    def test_rename_player_success(self):
        """Rename a player and preserve their points and games."""
        self.score.record_game("Lulu", 10)
        result = self.score.rename_player("Lulu", "Anastasia")
        self.assertTrue(result)
        self.assertIn("Anastasia", self.score.scores)
        self.assertNotIn("Lulu", self.score.scores)
        self.assertEqual(self.score.scores["Anastasia"]["total_points"], 10)

    def test_rename_player_merge_existing(self):
        """Rename to an existing player and merge total points and games."""
        self.score.record_game("Lulu", 10)
        self.score.record_game("Anastasia", 5)
        result = self.score.rename_player("Anastasia", "Lulu")
        self.assertTrue(result)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 15)
        self.assertEqual(len(self.score.scores["Lulu"]["games"]), 2)

    def test_rename_player_old_name_not_found(self):
        """Return False if the original player name does not exist."""
        result = self.score.rename_player("Nonexistent", "NewName")
        self.assertFalse(result)

    def test_rename_player_same_name_returns_true(self):
        """Return True when renaming a player to the same name."""
        self.score.record_game("Lulu", 10)
        result = self.score.rename_player("Lulu", "Lulu")
        self.assertTrue(result)
        self.assertIn("Lulu", self.score.scores)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 10)

    # --- clear_scores ------------------------------------------------------

    def test_clear_scores_empties_scores(self):
        """Clear all player scores and verify empty dictionary."""
        self.score.record_game("Lulu", 10)
        self.score.clear_scores()
        self.assertEqual(self.score.scores, {})
        self.mock_json_dump.assert_called()

    # --- Edge cases -------------------------------------------------------

    def test_record_game_zero_or_negative_points(self):
        """Record zero or negative points and retain values correctly."""
        self.score.record_game("Lulu", 0)
        self.score.record_game("Anastasia", -5)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 0)
        self.assertEqual(self.score.scores["Anastasia"]["total_points"], -5)


if __name__ == "__main__":
    unittest.main()
