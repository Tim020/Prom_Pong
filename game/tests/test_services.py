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
        code = escape.move_cursor()
        self.assertEqual(code, "\033[0;0H")

    def test_move_cursor_args(self):
        """
        .move_cursor should return the sequence to move the char to the given args
        """
        x = 12
        y = 8
        code = escape.move_cursor(x, y)
        self.assertEqual(code, "\033[{};{}H".format(y, x))

    def test_move_cursor_illegal_args(self):
        """
        .move_cursor should raise an exception if the args given to it are illegal, eg. out of range
        """
        with self.assertRaises(ValueError):
            escape.move_cursor(120, 90)
            escape.move_cursor(-1, 0)
            escape.move_cursor(0, 180)

        with self.assertRaises(TypeError):
            escape.move_cursor(0.5, 2)
            escape.move_cursor("0", "2")

    def test_set_graphics(self):
        """
        .set_graphics should return the sequence to change the settings given in the args
        """
        attr = 8
        fore = 30
        back = 40
        code = escape.set_graphics(attr, fore, back)
        self.assertEqual(code, "\033[{};{};{}m".format(attr, fore, back))

    def test_set_graphics_illegal_args(self):
        """
        .set_graphics should raise an exception if the args given to it are illegal
        """
        with self.assertRaises(ValueError):
            escape.set_graphics(3, 30, 40)
            escape.set_graphics(0, -4, 47)
            escape.set_graphics(0, 33, 50)

        with self.assertRaises(TypeError):
            escape.set_graphics("0", "30", 47)
            escape.set_graphics(0.0, 30.1, 47.0)


class TestButtonListenerDebounce(TestCase):
    button = ButtonListener(_getter, _callback)

    def test_constructor(self):
        self.assertEqual(self.button.cb(), _callback())
        self.assertEqual(self.button._getter(), _getter())
        self.assertTrue(self.button._debounce)


class TestButtonListenerNoDebounce(TestCase):
    button = ButtonListener(_getter, _callback, False)
