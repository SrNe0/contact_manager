"""Tests for app.main."""

import contextlib
import io
import unittest
from unittest import mock

from app import main as app_main

ANA = {"id": 1, "name": "Ana", "phone": "111", "email": "ana@example.com"}


class MainTests(unittest.TestCase):
    def run_main(self, inputs, loaded=([ANA], None)):
        output = io.StringIO()
        with mock.patch.object(app_main, "load_contacts", return_value=loaded), \
                mock.patch("builtins.input", side_effect=inputs), \
                contextlib.redirect_stdout(output):
            code = app_main.main()
        return code, output.getvalue()

    def test_exit_option(self):
        code, output = self.run_main(["7"])
        self.assertEqual(code, 0)
        self.assertIn("Welcome to Contact Manager", output)
        self.assertIn("Thank you", output)

    def test_invalid_option_shows_valid_range(self):
        _, output = self.run_main(["9", "", "7"])
        self.assertIn("Please select 1-7", output)

    def test_runs_selected_action(self):
        _, output = self.run_main(["2", "", "7"])
        self.assertIn("[1] Ana", output)

    def test_ctrl_c_and_end_of_input_exit_cleanly(self):
        for error in (KeyboardInterrupt, EOFError):
            with self.subTest(error=error.__name__):
                code, output = self.run_main(error)
                self.assertEqual(code, 0)
                self.assertIn("Thank you", output)

    def test_load_warning_waits_before_menu_clears_screen(self):
        _, output = self.run_main(["", "7"], loaded=([], "file is damaged"))
        self.assertLess(output.index("file is damaged"), output.index("\033[2J"))

    def test_load_failure_closes_instead_of_starting_empty(self):
        output = io.StringIO()
        with mock.patch.object(
            app_main, "load_contacts", side_effect=PermissionError("denied")
        ), mock.patch("builtins.input") as prompt, contextlib.redirect_stdout(output):
            code = app_main.main()

        self.assertEqual(code, 1)
        prompt.assert_not_called()
        self.assertIn("Could not load", output.getvalue())


if __name__ == "__main__":
    unittest.main()
