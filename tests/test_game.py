# tests/test_game.py
"""Tests for the PigGame interactive loop with safe I/O mocking."""
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
    def setUp(self):
        # Real players (predictable state)
        self.p1 = Player("P1", is_ai=False)
        self.p2 = Player("P2", is_ai=False)

        # Mocks for collaborators passed via constructor
        self.score = MagicMock()
        self.dice = MagicMock()
        self.ai = MagicMock()

        # Default die: return [3] unless overridden in a test
        self.dice.roll.return_value = [3]

        # Game with low winning score to keep tests short
        self.game = PigGame(
            [self.p1, self.p2],
            self.score,
            winning_score=10,
            dice_hand=self.dice,
            ai_agent=self.ai,
        )

    # Utility: run play() with scripted inputs and capture stdout
    def run_game_with_inputs(self, inputs):
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch("sys.stdout", new=out):
            self.game.play()
        return out.getvalue()

    # 1) Roll then hold: bank points and switch turn
    def test_roll_then_hold_banks_points_and_switches_turn(self):
        out = self.run_game_with_inputs(["r", "h", "q"])
        self.assertIn("rolled 3", out)
        self.assertIn("banks 3 points", out)
        self.assertEqual(self.p1.get_score(), 3)
        self.assertIn("Quitting current game", out)

    # 2) Rolling a 1 ends turn and loses turn total
    def test_roll_one_ends_turn_and_loses_turn_total(self):
        self.dice.roll.return_value = [1]
        out = self.run_game_with_inputs(["r", "q"])
        self.assertIn("rolled 1", out)
        self.assertIn("Turn lost", out)
        self.assertEqual(self.p1.get_score(), 0)

    # 3) Cheat wins and records game
    def test_cheat_wins_and_records_game(self):
        self.game.winning_score = 10
        out = self.run_game_with_inputs(["c"])
        self.assertIn("Cheat used! Adding 50 points", out)
        self.assertIn("wins by cheat", out)
        self.score.record_game.assert_called_once()
        args, _ = self.score.record_game.call_args
        self.assertEqual(args[0], "P1")
        self.assertGreaterEqual(args[1], 50)

    # 4) Name change preserves stats via score.rename_player
    def test_name_change_calls_score_manager_and_updates_player(self):
        self.p1.add_score(4)
        out = self.run_game_with_inputs(["name", "NewName", "q"])
        self.assertTrue(("Renamed P1 -> NewName" in out) or ("Renamed P1 → NewName" in out))
        self.score.rename_player.assert_called_once_with("P1", "NewName")
        self.assertEqual(self.p1.get_name(), "NewName")

    # 5) Help shows help text and reprompts
    def test_help_command_shows_text_then_quit(self):
        out = self.run_game_with_inputs(["help", "q"])
        self.assertIn("Commands during your turn", out)
        self.assertTrue(("r, roll" in out) or ("roll the die" in out))

    # 6) Invalid command reprompts safely
    def test_invalid_command_is_reprompted(self):
        out = self.run_game_with_inputs(["x", "?", "q"])
        self.assertIn("Unknown command", out)
        self.assertTrue(("Commands during your turn" in out) or ("HELP" in out))
        self.assertIn("Quitting current game", out)

    # 7) AI difficulty change path (when any AI exists)
    def test_ai_difficulty_change_when_ai_exists(self):
        self.p2.is_ai = True
        out = self.run_game_with_inputs(["ai", "hard", "q"])
        self.assertTrue(("AI difficulty set to hard" in out) or ("set to hard" in out))
        self.game.ai_agent.set_difficulty.assert_called_once_with("hard")

    # 8) Restart resets both players' scores
    def test_restart_resets_scores(self):
        self.p1.set_score(7)
        self.p2.set_score(5)
        out = self.run_game_with_inputs(["restart", "q"])
        self.assertTrue(("Restarting current match" in out) or ("scores reset" in out))
        self.assertEqual(self.p1.get_score(), 0)
        self.assertEqual(self.p2.get_score(), 0)

    # 9) Human win occurs immediately after a roll reaches threshold (auto-win on roll)
    def test_human_win_by_reaching_threshold_during_roll(self):
        self.game.winning_score = 7
        self.dice.roll.return_value = [7]
        out = self.run_game_with_inputs(["r"])
        self.assertIn("reaches 7 points and wins!", out)
        self.score.record_game.assert_called_once()
        args, _ = self.score.record_game.call_args
        self.assertEqual(args[0], "P1")
        self.assertGreaterEqual(args[1], 7)

    # 10) AI player can win by rolling (no user input)
    def test_ai_can_win_by_rolling_and_records_game(self):
        self.p1.is_ai = True
        self.ai.decide.return_value = "roll"
        self.dice.roll.return_value = [10]
        out = self.run_game_with_inputs([])  # AI-only path
        self.assertIn("AI decides to roll", out)
        self.assertIn("wins", out)
        self.score.record_game.assert_called_once()
        args, _ = self.score.record_game.call_args
        self.assertEqual(args[0], "P1")
        self.assertGreaterEqual(args[1], 10)

    # --- Extra safety / edge-path coverage --------------------------------

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

    # Constructor validation (must be exactly two players)
    def test_init_raises_when_not_two_players(self):
        p1 = Player("A")
        score = Score()
        with self.assertRaises(ValueError):
            PigGame([p1], score)  # only one player

    # _prompt_cmd KeyboardInterrupt path -> returns "quit"
    def test_prompt_cmd_keyboardinterrupt_returns_quit(self):
        g = PigGame([Player("A"), Player("B")], Score())
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            self.assertEqual(g._prompt_cmd(), "quit")

    # _prompt_ai_level EOFError path -> None and "cancelled" printed
    def test_prompt_ai_level_eof_returns_none_and_prints_cancelled(self):
        g = PigGame([Player("A"), Player("B")], Score())
        out = io.StringIO()
        with patch("builtins.input", side_effect=EOFError), patch("sys.stdout", new=out):
            lvl = g._prompt_ai_level()
        self.assertIsNone(lvl)
        self.assertIn("cancel", out.getvalue().lower())

    # Hold path triggers "wins with ..." branch (not auto-win-on-roll)
    def test_hold_can_win_and_records_game(self):
        # Make P1 already at threshold; hold adds 0 but still wins via hold branch
        self.p1.set_score(10)
        g = PigGame([self.p1, self.p2], Score(), winning_score=10, dice_hand=self.dice, ai_agent=self.ai)
        out = io.StringIO()
        with patch("builtins.input", side_effect=["h"]), patch("sys.stdout", new=out), \
             patch.object(g.score_manager, "record_game") as rec:
            g.play()
        self.assertIn("wins with", out.getvalue())
        rec.assert_called_once()
        args, _ = rec.call_args
        self.assertEqual(args[0], "P1")
        self.assertGreaterEqual(args[1], 10)

    # Safe when DiceHand.roll() returns [] (roll value None -> '?' face + guarded turn loss)
    def test_roll_none_values_is_safe_and_shows_question_mark(self):
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
    # Covers _prompt_ai_level invalid branch before a valid selection
        self.p2.is_ai = True
        out = self.run_game_with_inputs(["ai", "impossible", "hard", "q"])
        self.assertIn("Invalid difficulty", out)
        self.game.ai_agent.set_difficulty.assert_called_once_with("hard")

    def test_ai_change_when_no_ai_exists_shows_info(self):
        # Covers info message when user tries to change AI with no AI opponent
        self.p2.is_ai = False
        out = self.run_game_with_inputs(["ai", "q"])
        self.assertIn("AI difficulty can only be changed", out)

    def test_name_change_keyboardinterrupt_cancel(self):
        # Covers the KeyboardInterrupt path in the name change prompt
        out = io.StringIO()
        with patch("builtins.input", side_effect=["name", KeyboardInterrupt, "q"]), patch("sys.stdout", new=out):
            self.game.play()
        self.assertIn("Name change cancelled", out.getvalue())

    def test_name_change_no_previous_stats_message(self):
        # Covers rename_player returning False -> "No previous stats existed" branch
        self.game.score_manager.rename_player.return_value = False
        out = self.run_game_with_inputs(["name", "Neo", "q"])
        self.assertIn("No previous stats existed", out)


if __name__ == "__main__":
    unittest.main()
