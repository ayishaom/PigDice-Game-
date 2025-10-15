"""Unit tests for the main module: construction, execution, and guard behavior."""
import os
import sys
import io
import types
import importlib
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


class TestMainModule(unittest.TestCase):
    def setUp(self):
        # Ensure a fresh import context for each test
        if "main" in sys.modules:
            del sys.modules["main"]

    # --- Helpers ------------------------------------------------------------

    def _import_main(self):
        """Import the main module freshly."""
        import main
        return sys.modules["main"]

    # --- Tests --------------------------------------------------------------

    def test_importing_main_does_not_run_program(self):
        """Importing the module (name == 'main') must NOT start the menu loop."""
        with patch("menu.Menu") as MockMenu:
            mod = self._import_main()
        self.assertTrue(hasattr(mod, "main"))
        self.assertTrue(callable(mod.main))
        self.assertFalse(MockMenu.called)

    def test_main_constructs_menu_and_runs_once(self):
        """main() should instantiate Menu() and call run() exactly once."""
        mod = self._import_main()
        with patch("main.Menu") as MockMenu:
            instance = MockMenu.return_value
            ret = mod.main()
        self.assertIsNone(ret)
        MockMenu.assert_called_once_with()
        instance.run.assert_called_once_with()

    def test_main_returns_none(self):
        """main() has no return value (explicitly None)."""
        mod = self._import_main()
        with patch("main.Menu") as MockMenu:
            result = mod.main()
        self.assertIsNone(result)
        self.assertEqual(MockMenu.call_count, 1)
        self.assertEqual(MockMenu.return_value.run.call_count, 1)

    def test_multiple_main_calls_create_new_menu_each_time(self):
        """Each call to main() creates a new Menu instance (no reuse)."""
        mod = self._import_main()
        with patch("main.Menu") as MockMenu:
            mod.main()
            mod.main()
        self.assertEqual(MockMenu.call_count, 2)
        self.assertEqual(MockMenu.return_value.run.call_count, 2)

    def test_main_propagates_keyboard_interrupt(self):
        """Exceptions in Menu.run (e.g., KeyboardInterrupt) should propagate (no swallow)."""
        mod = self._import_main()
        with patch("main.Menu") as MockMenu:
            MockMenu.return_value.run.side_effect = KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):
                mod.main()
        MockMenu.assert_called_once()

    def test_main_propagates_generic_exception(self):
        """Generic errors from Menu.run should also propagate."""
        mod = self._import_main()
        with patch("main.Menu") as MockMenu:
            MockMenu.return_value.run.side_effect = ValueError("boom")
            with self.assertRaises(ValueError):
                mod.main()
        MockMenu.assert_called_once()

    def test_main_prints_nothing(self):
        """main() itself should not print; any output is owned by Menu.run()."""
        mod = self._import_main()
        with patch("main.Menu") as MockMenu, patch("sys.stdout", new=io.StringIO()) as out:
            MockMenu.return_value.run.side_effect = lambda: None
            mod.main()
            self.assertEqual(out.getvalue(), "")

    def test_main_signature_has_no_parameters(self):
        """main() is a zero-arg function (simple entrypoint)."""
        mod = self._import_main()
        import inspect
        sig = inspect.signature(mod.main)
        self.assertEqual(len(sig.parameters), 0)

    def test_reload_main_does_not_run_program(self):
        """Reloading the module (name == 'main') must not execute the program."""
        # First import
        mod1 = self._import_main()
        with patch("menu.Menu") as MockMenu:
            # Reload executes module body again, but guard prevents running
            mod2 = importlib.reload(mod1)
        self.assertIs(mod1, mod2)
        self.assertFalse(MockMenu.called)

    def test_run_as_script_guard_invokes_main(self):
        """
        Simulate running the file as a script by executing the module with __name__='__main__'.
        Then ensure Menu() is constructed and run() called.
        """
        import runpy
        # Ensure fresh state and patch after import resolution
        path_to_main = os.path.join(os.path.dirname(__file__), "..", "src", "main.py")
        path_to_main = os.path.abspath(path_to_main)

        # We need to patch 'menu.Menu' because main.py does 'from menu import Menu'
        with patch("menu.Menu") as MockMenu:
            # Execute the file as if it were run with `python main.py`
            runpy.run_path(path_to_main, run_name="__main__")
            self.assertTrue(MockMenu.called)
            self.assertGreaterEqual(MockMenu.return_value.run.call_count, 1)

    def test_menu_instantiation_has_no_arguments(self):
        """Verify main() constructs Menu with no args to avoid hidden coupling."""
        mod = self._import_main()
        with patch("main.Menu") as MockMenu:
            mod.main()
            # Ensure no positional/keyword arguments were passed to Menu()
            args, kwargs = MockMenu.call_args
            self.assertEqual(args, ())
            self.assertEqual(kwargs, {})


if __name__ == "__main__":
    unittest.main()
