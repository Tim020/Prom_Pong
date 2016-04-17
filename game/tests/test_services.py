from unittest import TestCase
from game.services import ANSIEscape, ButtonListener


escape = ANSIEscape()


def _getter():
    return 0


def _callback():
    return "This is the callback"


class TestANSIEscape(TestCase):
    def test_clear_screen(self):
        """
        ANSIEscape.clear_screen() should return the escape sequence for clearing the screen
        """
        code = escape.clear_screen()
        self.assertEqual(code, "\033[2J")

    def test_move_cursor_no_args(self):
        """
        .move_cursor should return the sequence for moving the cursor when it is given no args
        """
        code = escape.set_cursor_position()
        self.assertEqual(code, "\033[0;0f")

    def test_move_cursor_args(self):
        """
        .move_cursor should return the sequence to move the char to the given args
        """
        x = 12
        y = 8
        code = escape.set_cursor_position(x, y)
        self.assertEqual(code, "\033[{};{}f".format(y, x))

    def test_move_cursor_illegal_args(self):
        """
        .move_cursor should raise an exception if the args given to it are illegal, eg. out of range
        """
        with self.assertRaises(ValueError):
            escape.set_cursor_position(120, 90)
            escape.set_cursor_position(-1, 0)
            escape.set_cursor_position(0, 180)

        with self.assertRaises(TypeError):
            escape.set_cursor_position(0.5, 2)
            escape.set_cursor_position("0", "2")


class TestButtonListenerDebounce(TestCase):
    button = ButtonListener(_getter, _callback)

    def test_constructor(self):
        self.assertEqual(self.button.cb(), _callback())
        self.assertEqual(self.button._getter(), _getter())
        self.assertTrue(self.button._debounce)


class TestButtonListenerNoDebounce(TestCase):
    button = ButtonListener(_getter, _callback, False)

    def test_constructor(self):
        self.assertEqual(self.button.cb(), _callback())
        self.assertEqual(self.button._getter(), _getter())
        self.assertFalse(self.button._debounce)
