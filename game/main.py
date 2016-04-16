from serial import Serial
from services import ANSIEscape

debug = True

# Size of the window
window_size = [80, 20]
# Number of serves each player has
serves = [5, 5]
# Current score of each player
score = [0, 0]
# Size of the player's bats
bat_size = [4, 4]
# Top position of the bat for each player
bat_position = [3, 78]
# Ball position
ball_position = [0, 0]
# Ball motion
ball_motion = [0, 0]


def output(seq):
    if debug:
        print(repr(seq))
    else:
        serialPort.write(seq)


if not debug:
    # Open Pi serial port, speed 9600 bits per second
    serialPort = Serial("/dev/ttyAMA0", 57600)

    # Should not need, but just in case
    if not serialPort.isOpen():
        serialPort.open()

# Initial clear of the screen
output(ANSIEscape.clear_screen())
output(ANSIEscape.reset_cursor())

# Set the background colour
output("\033[42m")

# Draw the background colour
for i in range(0, window_size[1]):
    output(" " * window_size[0])

# Draw bats for player 1 and 2
output(ANSIEscape.draw_bat(bat_position[0], (window_size[1] - bat_size[0]) / 2))
output(ANSIEscape.draw_bat(bat_position[1], (window_size[1] - bat_size[1]) / 2))

# Change background colour and draw the net
output("\033[47m")
for i in range(0, window_size[1] / 4):
    output(ANSIEscape.set_cursor_position(window_size[0] / 2, 3 + (i * 4)) + " ")
    output(ANSIEscape.set_cursor_position(window_size[0] / 2, 4 + (i * 4)) + " ")

# Draw score for Player 1 and 2
output(ANSIEscape.get_numerical_text(score[0], 0))
output(ANSIEscape.get_numerical_text(score[1], 1))
