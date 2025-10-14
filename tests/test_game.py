"""Tests for the PigGame interactive loop with safe I/O mocking."""
import os
import sys
import io
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from game import PigGame
from player import Player

class TestPigGame(unittest.TestCase):
    def setUp(self):
        # Real players
        self.p1 = Player("P1", is_ai=False)
        self.p2 = Player("P2", is_ai=False)

        # Mocks for collaborators passed via constructor
        self.score = MagicMock()
        self.dice = MagicMock()
        self.ai = MagicMock()

        # Default single die returning 3 unless overridden per test
        self.dice.roll.return_value = [3]

        # Create game with a low winning score for faster tests where needed
        self.game = PigGame([self.p1, self.p2], self.score, winning_score=10, dice_hand=self.dice, ai_agent=self.ai)

    # Utility to run play() with inputs and capture stdout
    def run_game_with_inputs(self, inputs):
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch("sys.stdout", new=out):
            self.game.play()
        return out.getvalue()

    # 1) Roll then hold: banks points and switches turn
    def test_roll_then_hold_banks_points_and_switches_turn(self):
        # p1: roll(3) -> hold => total +3, then quit on p2 turn
        out = self.run_game_with_inputs(["r", "h", "q"])
        self.assertIn("rolled 3", out)
        self.assertIn("banks 3 points", out)
        self.assertEqual(self.p1.get_score(), 3)
        # After p1 turn ends, it's p2's turn when 'q' is consumed
        self.assertIn("Quitting current game", out)

    # 2) Rolling a 1 loses the turn and gives 0
    def test_roll_one_ends_turn_and_loses_turn_total(self):
        self.dice.roll.return_value = [1]
        out = self.run_game_with_inputs(["r", "q"])
        self.assertIn("rolled 1", out)
        self.assertIn("Turn lost", out)
        self.assertEqual(self.p1.get_score(), 0)

    # 3) Cheat adds 50; with winning_score=10 it wins and records game
    def test_cheat_wins_and_records_game(self):
        self.game.winning_score = 10
        out = self.run_game_with_inputs(["c"])
        self.assertIn("Cheat used! Adding 50 points", out)
        self.assertIn("wins by cheat", out)
        self.score.record_game.assert_called_once()
        # Winner should be P1
        args, _ = self.score.record_game.call_args
        self.assertEqual(args[0], "P1")
        self.assertGreaterEqual(args[1], 50)

    # 4) Name change preserves stats via score.rename_player
    def test_name_change_calls_score_manager_and_updates_player(self):
        self.p1.add_score(4)
        out = self.run_game_with_inputs(["name", "NewName", "q"])
        self.assertIn("Renamed P1 -> NewName", out)
        self.score.rename_player.assert_called_once_with("P1", "NewName")
        self.assertEqual(self.p1.get_name(), "NewName")

    # 5) Help shows help text and reprompts without crashing
    def test_help_command_shows_text_then_quit(self):
        out = self.run_game_with_inputs(["help", "q"])
        self.assertIn("Commands during your turn", out)
        self.assertIn("r, roll", out)

    # 6) Invalid command reprompts safely
    def test_invalid_command_is_reprompted(self):
        out = self.run_game_with_inputs(["x", "?", "q"])
        self.assertIn("Unknown command", out)
        self.assertIn("Commands during your turn", out)  # from "?"
        self.assertIn("Quitting current game", out)

    # 7) AI difficulty change path
    def test_ai_difficulty_change_when_ai_exists(self):
        # Make P2 the AI so option is available when P1 is human (any AI exists)
        self.p2.is_ai = True
        out = self.run_game_with_inputs(["ai", "hard", "q"])
        self.assertIn("AI difficulty set to hard", out)
        self.game.ai_agent.set_difficulty.assert_called_once_with("hard")

    # 8) Restart resets both players' scores
    def test_restart_resets_scores(self):
        self.p1.set_score(7)
        self.p2.set_score(5)
        out = self.run_game_with_inputs(["restart", "q"])
        self.assertIn("Restarting current match", out)
        self.assertEqual(self.p1.get_score(), 0)
        self.assertEqual(self.p2.get_score(), 0)

    # 9) Human win occurs immediately when a roll reaches threshold (auto-win on roll)
    def test_human_win_by_reaching_threshold_during_roll(self):
        # Set threshold so a single roll wins.
        self.game.winning_score = 7
        self.dice.roll.return_value = [7]
        out = self.run_game_with_inputs(["r"])  # win happens after roll
        self.assertIn("reaches 7 points and wins!", out)
        self.score.record_game.assert_called_once()
        args, _ = self.score.record_game.call_args
        self.assertEqual(args[0], "P1")
        self.assertGreaterEqual(args[1], 7)

    # 10) AI player can win by rolling (no user input needed for AI turn)
    def test_ai_can_win_by_rolling_and_records_game(self):
        # Make P1 the AI and P2 human so first turn is AI
        self.p1.is_ai = True
        # AI decides to roll, and a high roll wins immediately (winning_score=10)
        self.ai.decide.return_value = "roll"
        self.dice.roll.return_value = [10]
        out = self.run_game_with_inputs([])  # no input needed; AI acts
        self.assertIn("AI decides to roll", out)
        self.assertIn("wins", out)
        self.score.record_game.assert_called_once()
        args, _ = self.score.record_game.call_args
        self.assertEqual(args[0], "P1")
        self.assertGreaterEqual(args[1], 10)

    # --- Extra assertions for safety / edge paths --------------------------

    def test_name_change_cancel_when_empty(self):
        out = self.run_game_with_inputs(["name", "", "q"])
        self.assertIn("Name change cancelled", out)
        self.assertEqual(self.p1.get_name(), "P1")

    def test_ai_change_cancel_when_empty(self):
        self.p2.is_ai = True
        out = self.run_game_with_inputs(["ai", "", "q"])
        self.game.ai_agent.set_difficulty.assert_not_called()
        self.assertIn("Quitting current game", out)
        self.assertNotIn("AI difficulty set to", out)

    def test_quit_command_exits_cleanly(self):
        out = self.run_game_with_inputs(["q"])
        self.assertIn("Quitting current game", out)


if __name__ == "__main__":
    unittest.main()
