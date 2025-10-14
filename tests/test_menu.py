import os, sys, io
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from menu import Menu


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.menu = Menu()

    def _run_with_inputs(self, inputs):
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch("sys.stdout", new=out):
            self.menu.run()
        return out.getvalue()

    def test_quit_immediately(self):
        out = self._run_with_inputs(["5"])
        self.assertIn("Goodbye", out)
        self.assertFalse(self.menu.running)

    @patch("menu.PigGame")         
    @patch("menu.Intelligence")    
    @patch("menu.Score")           
    @patch("menu.Player")          
    def test_single_player_defaults(self, MockPlayer, MockScore, MockIntelligence, MockPigGame):
        out = self._run_with_inputs(["1", "", "", "5"])
        self.assertTrue(MockPigGame.called)
        MockPigGame.return_value.play.assert_called_once()
        MockIntelligence.return_value.set_difficulty.assert_called_once_with("medium")
        self.assertIn("Play against computer", out)

    @patch("menu.PigGame")
    @patch("menu.Score")
    @patch("menu.Player")
    def test_two_player_defaults(self, MockPlayer, MockScore, MockPigGame):
        out = self._run_with_inputs(["2", "", "", "5"])
        self.assertTrue(MockPigGame.called)
        MockPigGame.return_value.play.assert_called_once()
        self.assertGreaterEqual(MockPlayer.call_count, 2)
        self.assertIn("two-player game", out)

    @patch("menu.Score")
    def test_high_scores_empty(self, MockScore):
        MockScore.return_value.get_high_scores.return_value = []
        out = self._run_with_inputs(["3", "5"])
        self.assertIn("No scores recorded yet", out)

    @patch("histogram.Histogram")  
    @patch("menu.Score")
    def test_high_scores_with_entries(self, MockScore, MockHistogram):
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
        out = self._run_with_inputs(["x", "5"])
        self.assertIn("Please enter a number between 1 and 5.", out)
        self.assertIn("Goodbye", out)

    def test_rules_shown_then_quit(self):
        out = self._run_with_inputs(["4", "5"])
        self.assertIn("PIG DICE — RULES", out)
        self.assertIn("Goodbye", out)

    @patch("menu.PigGame")
    @patch("menu.Intelligence")
    @patch("menu.Score")
    @patch("menu.Player")
    def test_single_player_invalid_then_valid_difficulty(self, MockPlayer, MockScore, MockIntelligence, MockPigGame):
        out = self._run_with_inputs(["1", "", "crazy", "hard", "5"])
        MockIntelligence.return_value.set_difficulty.assert_called_once_with("hard")
        self.assertTrue(MockPigGame.called)
        self.assertIn("Invalid difficulty", out)

    @patch("menu.PigGame")
    @patch("menu.Intelligence")
    @patch("menu.Score")
    @patch("menu.Player")
    def test_single_player_name_trims_and_default(self, MockPlayer, MockScore, MockIntelligence, MockPigGame):
        out = self._run_with_inputs(["1", "   Alice  ", "", "5"])
        first_call_args, first_call_kwargs = MockPlayer.call_args_list[0]
        self.assertEqual(first_call_args[0], "Alice")
        self.assertIn("Play against computer", out)
        MockIntelligence.return_value.set_difficulty.assert_called_once_with("medium")

    def test_keyboard_interrupt_exits_cleanly(self):
        import io
        out = io.StringIO()
        with patch("builtins.input", side_effect=KeyboardInterrupt), patch("sys.stdout", new=out):
            self.menu.run()
        self.assertFalse(self.menu.running)
        self.assertIn("Exiting… Goodbye.", out.getvalue())

if __name__ == "__main__":
    unittest.main()
