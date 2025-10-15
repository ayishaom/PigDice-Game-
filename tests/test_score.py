"""Unit tests for Score: recording, retrieving, renaming, clearing, and file interactions."""

import os
import sys
import unittest
from unittest.mock import mock_open, patch
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from score import Score


class TestScore(unittest.TestCase):
    """Covers initialization, recording games, retrieving scores, renaming, and clearing."""

    def setUp(self):
        # Patch open for all file operations to prevent disk I/O
        self.mock_open = mock_open()
        patcher = patch("builtins.open", self.mock_open)
        self.addCleanup(patcher.stop)
        self.mock_file = patcher.start()

        # Patch json.load and json.dump
        self.json_load_patcher = patch("json.load", return_value={})
        self.addCleanup(self.json_load_patcher.stop)
        self.mock_json_load = self.json_load_patcher.start()

        self.json_dump_patcher = patch("json.dump")
        self.addCleanup(self.json_dump_patcher.stop)
        self.mock_json_dump = self.json_dump_patcher.start()

        # Create Score instance
        self.score = Score(file_path="dummy.json")

    # Initialization & load 
    def test_initial_scores_empty_when_file_missing(self):
        self.mock_json_load.return_value = {}
        s = Score("nonexistent.json")
        self.assertEqual(s.scores, {})

    # record_game 

    def test_record_game_creates_new_player(self):
        self.score.record_game("Lulu", 10)
        self.assertIn("Lulu", self.score.scores)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 10)
        self.assertEqual(len(self.score.scores["Lulu"]["games"]), 1)
        self.mock_json_dump.assert_called()

    def test_record_game_multiple_entries_updates_total(self):
        self.score.record_game("Lulu", 10)
        self.score.record_game("Lulu", 5)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 15)
        self.assertEqual(len(self.score.scores["Lulu"]["games"]), 2)

    # get_high_scores 

    def test_get_high_scores_sorted_descending(self):
        self.score.record_game("Lulu", 10)
        self.score.record_game("Anastasia", 15)
        top_scores = self.score.get_high_scores()
        self.assertEqual(top_scores[0][0], "Anastasia")
        self.assertEqual(top_scores[1][0], "Lulu")

    #  get_player_history 

    def test_get_player_history_existing_player(self):
        self.score.record_game("Lulu", 7)
        history = self.score.get_player_history("Lulu")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["points"], 7)

    def test_get_player_history_nonexistent_player(self):
        history = self.score.get_player_history("Nonexistent")
        self.assertEqual(history, [])

    # rename_player 

    def test_rename_player_success(self):
        self.score.record_game("Lulu", 10)
        result = self.score.rename_player("Lulu", "Anastasia")
        self.assertTrue(result)
        self.assertIn("Anastasia", self.score.scores)
        self.assertNotIn("Lulu", self.score.scores)
        self.assertEqual(self.score.scores["Anastasia"]["total_points"], 10)

    def test_rename_player_merge_existing(self):
        self.score.record_game("Lulu", 10)
        self.score.record_game("Anastasia", 5)
        result = self.score.rename_player("Anastasia", "Lulu")
        self.assertTrue(result)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 15)
        self.assertEqual(len(self.score.scores["Lulu"]["games"]), 2)

    def test_rename_player_old_name_not_found(self):
        result = self.score.rename_player("Nonexistent", "NewName")
        self.assertFalse(result)

    def test_rename_player_same_name_returns_true(self):
        self.score.record_game("Lulu", 10)
        result = self.score.rename_player("Lulu", "Lulu")
        self.assertTrue(result)
        self.assertIn("Lulu", self.score.scores)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 10)

    # clear_scores 

    def test_clear_scores_empties_scores(self):
        self.score.record_game("Lulu", 10)
        self.score.clear_scores()
        self.assertEqual(self.score.scores, {})
        self.mock_json_dump.assert_called()

    # Edge cases 

    def test_record_game_zero_or_negative_points(self):
        self.score.record_game("Lulu", 0)
        self.score.record_game("Anastasia", -5)
        self.assertEqual(self.score.scores["Lulu"]["total_points"], 0)
        self.assertEqual(self.score.scores["Anastasia"]["total_points"], -5)


if __name__ == "__main__":
    unittest.main()
