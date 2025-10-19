"""Unit tests for Menu: options display, input handling, and game start."""

import os, sys, io
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from menu import Menu


class TestMenu(unittest.TestCase):
    """Test Menu behaviors including user prompts, game creation, and high scores."""

    def setUp(self):
        """Create a fresh Menu instance before each test."""
        self.menu = Menu()

    def _run_with_inputs(self, inputs):
        """Run the menu loop with scripted inputs and capture output.

        Args:
            inputs (list[str]): Simulated user input commands.

        Returns:
            str: Captured standard output from the menu loop.
        """
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch("sys.stdout", new=out):
            self.menu.run()
        return out.getvalue()

    def test_quit_immediately(self):
        """Exit immediately when user selects 'Quit'."""
        out = self._run_with_inputs(["5"])
        self.assertIn("Goodbye", out)
        self.assertFalse(self.menu.running)

    @patch("menu.PigGame")         
    @patch("menu.Intelligence")    
    @patch("menu.Score")           
    @patch("menu.Player")          
    def test_single_player_defaults(self, MockPlayer, MockScore, MockIntelligence, MockPigGame):
        """Start single-player game with default names and AI difficulty."""
        out = self._run_with_inputs(["1", "", "", "5"])
        self.assertTrue(MockPigGame.called)
        MockPigGame.return_value.play.assert_called_once()
        MockIntelligence.return_value.set_difficulty.assert_called_once_with("medium")
        self.assertIn("Play against computer", out)

    @patch("menu.PigGame")
    @patch("menu.Score")
    @patch("menu.Player")
    def test_two_player_defaults(self, MockPlayer, MockScore, MockPigGame):
        """Start two-player game with default names."""
        out = self._run_with_inputs(["2", "", "", "5"])
        self.assertTrue(MockPigGame.called)
        MockPigGame.return_value.play.assert_called_once()
        self.assertGreaterEqual(MockPlayer.call_count, 2)
        self.assertIn("two-player game", out)

    @patch("menu.Score")
    def test_high_scores_empty(self, MockScore):
        """Display message when no high scores exist."""
        MockScore.return_value.get_high_scores.return_value = []
        out = self._run_with_inputs(["3", "5"])
        self.assertIn("No scores recorded yet", out)

    @patch("histogram.Histogram")  
    @patch("menu.Score")
    def test_high_scores_with_entries(self, MockScore, MockHistogram):
        """Show high scores and histogram when entries exist."""
        MockScore.return_value.get_high_scores.return_value = [
            ("Ana", {"total_points": 120, "games": [{"date": "2025-10-01", "points": 60}]}),
            ("Ben", {"total_points": 90, "games": [{"date": "2025-10-02", "points": 45}]}),
        ]
        MockHistogram.return_value.generate_total.return_value = ["Ana | ******", "Ben | *****"]
        out = self._run_with_inputs(["3", "5"])
        self.assertIn("High Scores", out)
        self.assertIn("Ana", out)
        self.assertTrue(MockHistogram.called)

    def test_invalid_menu_choice_then_quit(self):
        """Reprompt for invalid menu choice and exit cleanly."""
        out = self._run_with_inputs(["x", "5"])
        self.assertIn("Please enter a number between 1 and 5.", out)
        self.assertIn("Goodbye", out)

    def test_rules_shown_then_quit(self):
        """Display game rules and then quit."""
        out = self._run_with_inputs(["4", "5"])
        self.assertIn("PIG DICE — RULES", out)
        self.assertIn("Goodbye", out)

    @patch("menu.PigGame")
    @patch("menu.Intelligence")
    @patch("menu.Score")
    @patch("menu.Player")
    def test_single_player_invalid_then_valid_difficulty(self, MockPlayer, MockScore, MockIntelligence, MockPigGame):
        """Warn on invalid AI difficulty and accept valid input."""
        out = self._run_with_inputs(["1", "", "crazy", "hard", "5"])
        MockIntelligence.return_value.set_difficulty.assert_called_once_with("hard")
        self.assertTrue(MockPigGame.called)
        self.assertIn("Invalid difficulty", out)

    @patch("menu.PigGame")
    @patch("menu.Intelligence")
    @patch("menu.Score")
    @patch("menu.Player")
    def test_single_player_name_trims_and_default(self, MockPlayer, MockScore, MockIntelligence, MockPigGame):
        """Trim whitespace from player name and use default AI difficulty."""
        out = self._run_with_inputs(["1", "   Alice  ", "", "5"])
        first_call_args, first_call_kwargs = MockPlayer.call_args_list[0]
        self.assertEqual(first_call_args[0], "Alice")
        self.assertIn("Play against computer", out)
        MockIntelligence.return_value.set_difficulty.assert_called_once_with("medium")

    def test_keyboard_interrupt_exits_cleanly(self):
        """Exit the menu loop safely on KeyboardInterrupt."""
        import io
        out = io.StringIO()
        with patch("builtins.input", side_effect=KeyboardInterrupt), patch("sys.stdout", new=out):
            self.menu.run()
        self.assertFalse(self.menu.running)
        self.assertIn("Exiting… Goodbye.", out.getvalue())

    def test_display_options_prints_menu_header(self):
        """Print the menu header correctly when displaying options."""
        m = Menu()
        out = io.StringIO()
        with patch("sys.stdout", new=out):
            m.display_options()
        text = out.getvalue()
        assert ("P I G   D I C E" in text) or ("MENU" in text) or ("🎲" in text)

    def test_prompt_difficulty_invalid_then_valid_prints_warning(self):
        """Warn on invalid difficulty input and return valid difficulty."""
        m = Menu()
        out = io.StringIO()
        with patch("builtins.input", side_effect=["crazy", "medium"]), patch("sys.stdout", new=out):
            level = m._prompt_difficulty("x: ", default="medium")
        assert level == "medium"
        assert "Invalid difficulty" in out.getvalue()

    def test_prompt_nonempty_name_whitespace_then_default_message_and_default_return(self):
        """Warn if player name is empty and return default name."""
        m = Menu()
        out = io.StringIO()
        with patch("builtins.input", side_effect=["   ", ""]), patch("sys.stdout", new=out):
            name = m._prompt_nonempty_name("name: ", default="PlayerX")
        assert name == "PlayerX"
        assert "Name cannot be empty" in out.getvalue()


if __name__ == "__main__":
    unittest.main()
