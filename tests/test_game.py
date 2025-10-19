"""Unit tests for PigGame interactive loop with safe I/O mocking.

Covers human and AI turns, rolling, holding, cheating, name changes, help commands,
AI difficulty settings, restart, winning conditions, and edge/error cases.
"""

import os
import sys
import io
import unittest
from unittest.mock import MagicMock, patch

# Path shim: adjust if your layout differs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from game import PigGame  # noqa: E402
from player import Player  # noqa: E402
from score import Score  # noqa: E402


class TestPigGame(unittest.TestCase):
    """Unit tests for the PigGame class covering I/O, turns, scoring, AI, and commands."""

    def setUp(self):
        """Set up two human players and a PigGame instance with mocked dice and AI agent."""
        self.p1 = Player("P1", is_ai=False)
        self.p2 = Player("P2", is_ai=False)
        self.score = MagicMock()
        self.dice = MagicMock()
        self.ai = MagicMock()
        self.dice.roll.return_value = [3]  # Default die roll
        self.game = PigGame(
            [self.p1, self.p2],
            self.score,
            winning_score=10,
            dice_hand=self.dice,
            ai_agent=self.ai,
        )

    def run_game_with_inputs(self, inputs):
        """Run the game loop with scripted user inputs and capture stdout.

        Args:
            inputs (list[str]): List of input strings to simulate user commands.

        Returns:
            str: Captured standard output during the game loop.
        """
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch("sys.stdout", new=out):
            self.game.play()
        return out.getvalue()

    # --- Individual test cases --------------------------------------------

    def test_roll_then_hold_banks_points_and_switches_turn(self):
        """Test that rolling then holding banks points and ends turn properly."""
        out = self.run_game_with_inputs(["r", "h", "q"])
        self.assertIn("rolled 3", out)
        self.assertIn("banks 3 points", out)
        self.assertEqual(self.p1.get_score(), 3)
        self.assertIn("Quitting current game", out)

    def test_roll_one_ends_turn_and_loses_turn_total(self):
        """Test that rolling a 1 ends the turn and zeroes turn total."""
        self.dice.roll.return_value = [1]
        out = self.run_game_with_inputs(["r", "q"])
        self.assertIn("rolled 1", out)
        self.assertIn("Turn lost", out)
        self.assertEqual(self.p1.get_score(), 0)

    def test_cheat_wins_and_records_game(self):
        """Test that using cheat adds points and triggers a win, recording the game."""
        self.game.winning_score = 10
        out = self.run_game_with_inputs(["c"])
        self.assertIn("Cheat used! Adding 50 points", out)
        self.assertIn("wins by cheat", out)
        self.score.record_game.assert_called_once()

    def test_name_change_calls_score_manager_and_updates_player(self):
        """Test renaming a player preserves stats and updates score manager."""
        self.p1.add_score(4)
        out = self.run_game_with_inputs(["name", "NewName", "q"])
        self.assertTrue(("Renamed P1 -> NewName" in out) or ("Renamed P1 → NewName" in out))
        self.score.rename_player.assert_called_once_with("P1", "NewName")
        self.assertEqual(self.p1.get_name(), "NewName")

    def test_help_command_shows_text_then_quit(self):
        """Test that help command prints instructions and allows continued play."""
        out = self.run_game_with_inputs(["help", "q"])
        self.assertIn("Commands during your turn", out)

    def test_invalid_command_is_reprompted(self):
        """Test that invalid commands are rejected and user is re-prompted."""
        out = self.run_game_with_inputs(["x", "?", "q"])
        self.assertIn("Unknown command", out)
        self.assertIn("Quitting current game", out)

    def test_ai_difficulty_change_when_ai_exists(self):
        """Test that AI difficulty change works when an AI opponent exists."""
        self.p2.is_ai = True
        out = self.run_game_with_inputs(["ai", "hard", "q"])
        self.assertTrue(("AI difficulty set to hard" in out) or ("set to hard" in out))
        self.game.ai_agent.set_difficulty.assert_called_once_with("hard")

    def test_restart_resets_scores(self):
        """Test that restart command resets both players' scores."""
        self.p1.set_score(7)
        self.p2.set_score(5)
        out = self.run_game_with_inputs(["restart", "q"])
        self.assertEqual(self.p1.get_score(), 0)
        self.assertEqual(self.p2.get_score(), 0)

    def test_human_win_by_reaching_threshold_during_roll(self):
        """Test that a player wins immediately if roll reaches winning score."""
        self.game.winning_score = 7
        self.dice.roll.return_value = [7]
        out = self.run_game_with_inputs(["r"])
        self.assertIn("reaches 7 points and wins!", out)
        self.score.record_game.assert_called_once()

    def test_ai_can_win_by_rolling_and_records_game(self):
        """Test that AI can win by rolling without user input and game is recorded."""
        self.p1.is_ai = True
        self.ai.decide.return_value = "roll"
        self.dice.roll.return_value = [10]
        out = self.run_game_with_inputs([])
        self.assertIn("AI decides to roll", out)
        self.assertIn("wins", out)
        self.score.record_game.assert_called_once()

    def test_name_change_cancel_when_empty(self):
        """Test that empty input during name change cancels the operation."""
        out = self.run_game_with_inputs(["name", "", "q"])
        self.assertIn("Name change cancelled", out)
        self.assertEqual(self.p1.get_name(), "P1")

    def test_ai_change_cancel_when_empty(self):
        """Test that empty input during AI difficulty change cancels the operation."""
        self.p2.is_ai = True
        out = self.run_game_with_inputs(["ai", "", "q"])
        self.game.ai_agent.set_difficulty.assert_not_called()

    def test_quit_command_exits_cleanly(self):
        """Test that quit command terminates the game loop cleanly."""
        out = self.run_game_with_inputs(["q"])
        self.assertIn("Quitting current game", out)

    def test_init_raises_when_not_two_players(self):
        """Test that PigGame raises ValueError if not exactly two players are provided."""
        p1 = Player("A")
        score = Score()
        with self.assertRaises(ValueError):
            PigGame([p1], score)

    def test_prompt_cmd_keyboardinterrupt_returns_quit(self):
        """Test that _prompt_cmd handles KeyboardInterrupt and returns 'quit'."""
        g = PigGame([Player("A"), Player("B")], Score())
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            self.assertEqual(g._prompt_cmd(), "quit")

    def test_prompt_ai_level_eof_returns_none_and_prints_cancelled(self):
        """Test that _prompt_ai_level returns None on EOFError and prints cancellation."""
        g = PigGame([Player("A"), Player("B")], Score())
        out = io.StringIO()
        with patch("builtins.input", side_effect=EOFError), patch("sys.stdout", new=out):
            lvl = g._prompt_ai_level()
        self.assertIsNone(lvl)
        self.assertIn("cancel", out.getvalue().lower())

    def test_hold_can_win_and_records_game(self):
        """Test that holding can trigger a win and records the game."""
        self.p1.set_score(10)
        g = PigGame([self.p1, self.p2], Score(), winning_score=10, dice_hand=self.dice, ai_agent=self.ai)
        out = io.StringIO()
        with patch("builtins.input", side_effect=["h"]), patch("sys.stdout", new=out), \
             patch.object(g.score_manager, "record_game") as rec:
            g.play()
        self.assertIn("wins with", out.getvalue())
        rec.assert_called_once()

    def test_roll_none_values_is_safe_and_shows_question_mark(self):
        """Test that DiceHand.roll() returning empty list is handled safely with '?'."""
        dice = MagicMock()
        dice.roll.return_value = []
        g = PigGame([Player("P1"), Player("P2")], Score(), dice_hand=dice, ai_agent=self.ai)
        out = io.StringIO()
        with patch("builtins.input", side_effect=["r", "q"]), patch("sys.stdout", new=out):
            g.play()
        text = out.getvalue()
        self.assertIn("rolled None ?", text)
        self.assertIn("Invalid roll. Turn lost.", text)

    def test_ai_level_invalid_then_valid_prints_warning(self):
        """Test that invalid AI difficulty input is rejected and valid input accepted."""
        self.p2.is_ai = True
        out = self.run_game_with_inputs(["ai", "impossible", "hard", "q"])
        self.assertIn("Invalid difficulty", out)
        self.game.ai_agent.set_difficulty.assert_called_once_with("hard")

    def test_ai_change_when_no_ai_exists_shows_info(self):
        """Test that attempting AI change with no AI opponent shows info message."""
        self.p2.is_ai = False
        out = self.run_game_with_inputs(["ai", "q"])
        self.assertIn("AI difficulty can only be changed", out)

    def test_name_change_keyboardinterrupt_cancel(self):
        """Test that KeyboardInterrupt during name change cancels the operation."""
        out = io.StringIO()
        with patch("builtins.input", side_effect=["name", KeyboardInterrupt, "q"]), patch("sys.stdout", new=out):
            self.game.play()
        self.assertIn("Name change cancelled", out.getvalue())

    def test_name_change_no_previous_stats_message(self):
        """Test that renaming a player with no previous stats shows the appropriate message."""
        self.game.score_manager.rename_player.return_value = False
        out = self.run_game_with_inputs(["name", "Neo", "q"])
        self.assertIn("No previous stats existed", out)


if __name__ == "__main__":
    """Run the PigGame unit tests."""
    unittest.main()
