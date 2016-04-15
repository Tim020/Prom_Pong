from unittest import TestCase
from game.services import ANSIEscape

escape = ANSIEscape()


class TestANSIEscape(TestCase):
    def test_clear_screen(self):
        """
        ANSIEscape.clear_screen() should return the escape sequence for clearing the screen
        """
        code = escape.clear_screen()
        self.assertEqual(code, "\e[2J")
