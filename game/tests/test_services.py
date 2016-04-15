from unittest import TestCase
from game.services import ANSIEscape

escape = ANSIEscape()

class test_ansi_escape(TestCase):
    def test_clear_screen(self):
        """
        ansi_escape.clear_screen() should return the escape sequence for clearing the screen
        """
        code = escape.clear_screen()
        self.assertEqual(code, "\e[2J")
