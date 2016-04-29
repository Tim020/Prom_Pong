import threading
import smbus
import RPi.GPIO as GPIO


class ANSIEscape:
    @staticmethod
    def reset_cursor():
        return "\033[0;0f"

    @staticmethod
    def clear_screen():
        return "\033[2J"

    @staticmethod
    def set_cursor_position(x=1, y=1):
        return "\033[{};{}f".format(int(y), int(x))

    @staticmethod
    def set_graphics(attr, fore, back):
        pass

    @staticmethod
    def draw_bat(start_x, start_y):
        # Set the background colour to be black
        ret_seq = "\033[40m"
        for i in range(0, 4):
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + i) + " "
        return ret_seq

    @staticmethod
    def undraw_bat(start_x, start_y):
        # Set the background colour to be green
        ret_seq = "\033[42m"
        for i in range(0, 4):
            ret_seq += ANSIEscape.set_cursor_position(start_x, start_y + i) + " "
        return ret_seq

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


class I2C:
    ADC_ADDRESS = 0x21
    bus = None

    def __init__(self):
        self.bus = smbus.SMBus(1)

    @staticmethod
    def endian_swap(raw):
        """
        16 bit endian swap
        :param raw: Raw 16 bit input (low:high)
        :return: Endian swap (high:low)
        """
        low = raw & 0x00FF
        high = raw & 0xFF00
        high >>= 8
        low <<= 8
        return low | high

    @staticmethod
    def mask_high(raw):
        return raw & 0x0FFF

    def get_adc_value(self, channel):
        """
        get the value of the the adc on a given channel
        :param channel: 1, 2, 3, or 4
        :return: the value as int, between 0 and 2812=(3416 - 604)
        """
        if channel == 1:
            command = 0x10
        elif channel == 2:
            command = 0x20
        elif channel == 3:
            command = 0x40
        elif channel == 4:
            command = 0x80
        else:
            raise ValueError("channel must be 1, 2, 3, or 4")

        # Tell the ADC to convert a specific channel
        self.bus.write_byte(self.ADC_ADDRESS, command)

        # Get the conversion (read always gets most recent conversion)
        data = self.bus.read_word_data(self.ADC_ADDRESS, 0x00)

        # Process the data
        data = self.endian_swap(data)
        data = self.mask_high(data)
        # 52 is the value we got for 0.5V, so subtract this so we can work from 0 rather than 52.
        data -= 52

        # 1538 is the range in the values the ADC can give us between 0.5V and 2.5V
        # If were out of the scaled range we specified, set to the max or min value for our range.
        if data < 0:
            data = 0
        elif data > 1538:
            data = 1538

        return data


class ButtonListener:
    channel = None
    edge = None
    callback = None

    def __init__(self, channel, edge, callback, debounce=True):
        """
        Creates a new button listener
        :param channel: The GPIO channel to watch
        :param edge: GPIO.RISING or GPIO.FALLING
        :param callback: Func to callback for when button is pressed. Must take a single paramater, the channel.
        :param debounce: Should the button be debounced?
        """
        self.channel = channel
        self.edge = edge
        self.callback = callback

        if debounce:
            self.start_detecting_db()
        else:
            self.start_detecting_no_db()

    def db_callback_wrapper(self, channel=None):
        """
        Removes event detection for 0.1 seconds after a rising edge to prevent multiple activations
        :param channel: GPIO events pass us this addition paramater.
        """
        GPIO.remove_event_detect(self.channel)
        threading.Timer(0.1, self.start_detecting_db).start()

    def start_detecting_no_db(self):
        """
        just a no args wrapper for add_event_detect so we can pass it to a func easier
        """
        GPIO.add_event_detect(self.channel, self.edge, self.callback)

    def start_detecting_db(self):
        """
        just a no args wrapper for add_event_detect so we can pass it to a func easier
        """
        GPIO.add_event_detect(self.channel, self.edge, self.db_callback_wrapper())
