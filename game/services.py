class ANSIEscape:
    @staticmethod
    def clear_screen():
        pass

    @staticmethod
    def move_cursor(x=0, y=0):
        pass

    @staticmethod
    def set_graphics(attr, fore, back):
        pass


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
