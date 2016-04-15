class ANSIEscape:
    @staticmethod
    def reset_cursor():
        return "\033[0;0f"

    @staticmethod
    def clear_screen():
        return "\033[2J"

    @staticmethod
    def move_cursor(x=1, y=1):
        return "\033[" + str(y) + ";" + str(x) + "f"

    @staticmethod
    def set_graphics(attr, fore, back):
        pass

    @staticmethod
    def get_numerical_text(number, player):
        if player == 0:
            start_x = 29
        else:
            start_x = 48

        start_y = 2
        ret_seq = "\033[47m"
        ret_seq += ANSIEscape.move_cursor(start_x, start_y)
        if number == 0:
            ret_seq += "   "
            for i in range(0, 3):
                start_y += 1
                ret_seq += ANSIEscape.move_cursor(start_x, start_y)
                ret_seq += " "
                start_x += 2
                ret_seq += ANSIEscape.move_cursor(start_x, start_y)
                ret_seq += " "
                start_x -= 2
                ret_seq += ANSIEscape.move_cursor(start_x, start_y)
            start_y += 1
            ret_seq += ANSIEscape.move_cursor(start_x, start_y)
            ret_seq += "   "
        elif number == 1:
            ret_seq += ANSIEscape.move_cursor(start_x + 3, start_y)
            for i in range(0, 5):
                ret_seq += ANSIEscape.move_cursor(start_x, start_y + i)
                ret_seq += " "
        elif number == 2:
            pass
        elif number == 3:
            pass
        elif number == 4:
            pass
        elif number == 5:
            pass
        elif number == 6:
            pass
        elif number == 7:
            pass
        elif number == 8:
            pass
        elif number == 9:
            pass
        return ret_seq


class ButtonListener:
    _getter = None
    cb = None
    _debounce = True

    def __init__(self, getter, cb, debounce=True):
        """
        Creates a new button listener
        :param getter: a getter function for the button you want to watch
        :param cb: a callback function to execute when the button is pressed
        :param debounce: should the button listener perform a software debounce?
        """
        self._getter = getter
        self.cb = cb
        self._debounce = debounce
