from serial import Serial
from services import ANSIEscape

debug = True

# Number of serves each player has
serves = [5, 5]
# Current score of each player
score = [0, 0]
# Top position of the bat for each player
position = [3, 78]


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
for i in range(0, 20):
    output(" " * 80)

# Draw bats for player 1 and 2
output(ANSIEscape.draw_bat(position[0], 8))
output(ANSIEscape.draw_bat(position[1], 8))

# Change background colour and draw the net
output("\033[47m")
for i in range(0, 5):
    output(ANSIEscape.set_cursor_position(40, 3 + (i * 4)) + " ")
    output(ANSIEscape.set_cursor_position(40, 4 + (i * 4)) + " ")

# Draw score for Player 1 and 2
output(ANSIEscape.get_numerical_text(score[0], 0))
output(ANSIEscape.get_numerical_text(score[1], 1))
