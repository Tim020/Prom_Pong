from serial import Serial
from services import ANSIEscape
import time

debug = True

# Size of the window
window_size = [80, 20]
# Number of serves each player has
serves = [5, 5]
# Current score of each player
score = [0, 0]
# Size of the player's bats
bat_size = [4, 4]
# Top position of the bat for each player (initially in the middle)
bat_position = [(window_size[1] - bat_size[0]) / 2, (window_size[1] - bat_size[0]) / 2]
# Ball position
ball_position = [5, 8]
# Ball motion
ball_motion = [1, 0]

update_freq = float(2) / window_size[0]
last_time = time.time()
timer = time.time()
delta = 0
updates = 0


# Used when sending commands to the serial port, send to the console if in a dev environment (ie not on a Pi)
def output(seq):
    if debug:
        pass
        #print(repr(seq))
    else:
        serialPort.write(seq)


# Move the ball by motion and re-draws it
def move_and_draw_ball():
    global ball_position
    global ball_motion
    # First "un-draw" the current ball
    output(ANSIEscape.set_cursor_position(ball_position[0], ball_position[1]))
    output("\033[42m")
    output(" ")
    # Then update the ball position
    ball_position[0] += ball_motion[0]
    ball_position[1] += ball_motion[1]
    # Finally draw the new ball
    output(ANSIEscape.set_cursor_position(ball_position[0], ball_position[1]))
    output("\033[47m")
    output(" ")


# Checks if the ball has hit the top or bottom edge and updates the motion as appropriate
def check_wall_collision():
    global ball_position
    global window_size
    global ball_motion
    # Is the ball at the top or bottom edge (ignore x position)
    if ball_position[1] == 1 or ball_position[1] == window_size[1]:
        ball_motion[1] *= -1


# Checks if the ball has hit a paddle and updates the motion as appropriate
def check_paddle_collision():
    global ball_position
    global bat_position
    global bat_size
    global ball_motion
    if ball_position[0] == 4:
        if bat_position[0] <= ball_position[1] <= bat_position[0] + bat_size[0]:
            ball_motion[0] *= -1
    elif ball_position[0] == window_size[1] - 3:
        if bat_position[1] <= ball_position[1] <= bat_position[1] + bat_size[1]:
            ball_motion[0] *= -1


# Check if a point has been scored, returns true if there has
def check_point_scored():
    global ball_position
    global bat_position
    global bat_size
    global score
    if ball_position[0] == 4:
        if ball_position[1] < bat_position[0] or ball_position[1] > bat_position[0] + bat_size[0]:
            score[1] += 1
            return True
    elif ball_position[0] == window_size[1] - 3:
        if ball_position[1] < bat_position[1] or ball_position[1] > bat_position[1] + bat_size[1]:
            score[0] += 1
            return True
    return False


# Test code to see whether we are running properly on the Pi or not, opens the serial connection if we are
if not debug:
    # Open Pi serial port, speed 57600 bits per second
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
output(ANSIEscape.draw_bat(3, bat_position[0]))
output(ANSIEscape.draw_bat(window_size[0] - 2, bat_position[1]))

# Change background colour and draw the net
output("\033[47m")
for i in range(0, window_size[1] / 4):
    output(ANSIEscape.set_cursor_position(window_size[0] / 2, 3 + (i * 4)) + " ")
    output(ANSIEscape.set_cursor_position(window_size[0] / 2, 4 + (i * 4)) + " ")

# Draw score for Player 0 and 1
output(ANSIEscape.get_numerical_text(score[0], 0))
output(ANSIEscape.get_numerical_text(score[1], 1))


# Main loop for a single match (until a point is scored)
# Keeps a stable update rate to ensure the ball travels across the screen in 2 seconds
def match():
    global delta
    global last_time
    global updates
    global timer
    now = time.time()
    delta += (now - last_time) / update_freq
    last_time = now
    while delta >= 1:
        delta -= 1
        updates += 1
        move_and_draw_ball()
        check_wall_collision()
        check_paddle_collision()
        print("Ball Position: " + str(ball_position) + " | Ball Motion: " + str(ball_motion))
    if time.time() - timer > 1:
        print("UPS: " + str(updates))
        timer = time.time()
        updates = 0


# Main game loop:
# Runs while no player has a winning score
while score[0] < 10 and score[1] < 10:
    match()
