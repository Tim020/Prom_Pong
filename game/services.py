class ANSIEscape:
    @staticmethod
    def reset_cursor():
        return "\033[0;0f"

    @staticmethod
    def clear_screen():
        return "\033[2J"

    @staticmethod
    def set_cursor_position(x=1, y=1):
        return "\033[" + str(y) + ";" + str(x) + "f"

    @staticmethod
    def set_graphics(attr, fore, back):
        pass

    @staticmethod
    def get_numerical_text(number, player):
        # Determine the start position for the number based on which player it is for
        if player == 0:
            start_x = 29
        else:
            start_x = 48
        start_y = 2

        # Set the background colour to be white
        ret_seq = "\033[47m"

        # Move the cursor to the start position
        ret_seq += ANSIEscape.set_cursor_position(start_x, start_y)

        # Determine which number is required and get the sequence of characters to send to the serial port
        if number == 0:
            ret_seq += "   "
            for i in range(0, 3):
                start_y += 1
                ret_seq += ANSIEscape.set_cursor_position(start_x, start_y)
                ret_seq += " "
                start_x += 2
                ret_seq += ANSIEscape.set_cursor_position(start_x, start_y)
                ret_seq += " "
                start_x -= 2
                ret_seq += ANSIEscape.set_cursor_position(start_x, start_y)
            start_y += 1
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y)
            ret_seq += "   "
        elif number == 1:
            ret_seq += ANSIEscape.set_cursor_position(start_x + 3, start_y)
            for i in range(0, 5):
                ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + i)
                ret_seq += " "
        elif number == 2:
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 2)
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 4)
            ret_seq += "   "
        elif number == 3:
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 2)
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 4)
            ret_seq += "   "
        elif number == 4:
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 2)
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 3, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 3, start_y + 4)
            ret_seq += " "
        elif number == 5:
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 2)
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 4)
            ret_seq += "   "
        elif number == 6:
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 2)
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 4)
            ret_seq += "   "
        elif number == 7:
            ret_seq += "   "
            for i in range(1, 5):
                ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + i)
                ret_seq += " "
        elif number == 8:
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 2)
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 4)
            ret_seq += "   "
        elif number == 9:
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 1)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + 2)
            ret_seq += "   "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 3)
            ret_seq += " "
            ret_seq += ANSIEscape.set_cursor_position(start_x + 2, start_y + 4)
            ret_seq += " "
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
