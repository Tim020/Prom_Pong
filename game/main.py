from serial import Serial
from services import ANSIEscape, I2C
from PyGlow import PyGlow
import time
import smbus
import random
import RPi.GPIO as GPIO

debug = False

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
# Which player has the serve?
player_serve = 0
# How many pixels per LED?
led_steps = int((window_size[0]) / 8)
# The GPIO pins associated with the 8 LEDs
leds = [5, 6, 12, 13, 16, 19, 20, 26]
# Which LED is currently active
active_led = 0
# Stores the positions of the net, used for re-drawing when the ball goes through it
net_pos = []

update_freq = float(10) / window_size[0]
last_time = time.time()
timer = time.time()
delta = 0
updates = 0
I2CADDRESS = 0x21


# Used when sending commands to the serial port, send to the console if in a dev environment (ie not on a Pi)
def output(seq):
    if debug:
        pass
        # print(repr(seq))
    else:
        serialPort.write(seq)

# Undraw and re-draw the players scores
def print_score():
    global score
    output("\033[42m")
    for y in range(0, 5):
        output(ANSIEscape.set_cursor_position(29, 2 + y))
        output(" " * 3)
    for y in range(0, 5):
        output(ANSIEscape.set_cursor_position(48, 2 + y))
        output(" " * 3)
    output(ANSIEscape.get_numerical_text(score[0], 0))
    output(ANSIEscape.get_numerical_text(score[1], 1))

# Move the ball by motion and re-draws it
def move_and_draw_ball():
    global ball_position
    global ball_motion
    global active_led
    global leds
    global led_steps
    # First "un-draw" the current ball
    output(ANSIEscape.set_cursor_position(ball_position[0], ball_position[1]))
    # Check what colour to re-draw the background pixel with (ie is the ball "in" the net?)
    if ball_position[0] == window_size[0] / 2 and ball_position[1] in net_pos:
        output("\033[47m")
    else:
        output("\033[42m")
    output(" ")
    # Then update the ball position
    ball_position[0] += ball_motion[0]
    ball_position[1] += ball_motion[1]
    # Update the onboard LED
    GPIO.output(leds[active_led], False)
    active_led = ball_position[0]/led_steps
    GPIO.output(leds[active_led], True)
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
            ball_motion[1] = random.choice([-1, -1, 0, 1, 1])
    elif ball_position[0] == window_size[0] - 3:
        if bat_position[1] <= ball_position[1] <= bat_position[1] + bat_size[1]:
            ball_motion[0] *= -1
            ball_motion[1] = random.choice([-1, -1, 0, 1, 1])

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
    elif ball_position[0] == window_size[0] - 3:
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
    bus = smbus.SMBus(1)
    pyglow = PyGlow()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in leds:
        GPIO.setup(i, GPIO.OUT)

# Initial clear of the screen and hide the cursor
output(ANSIEscape.clear_screen())
output(ANSIEscape.reset_cursor())
output("\033[?25l")

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
    net_pos.append(3 + (i * 4))
    net_pos.append(4 + (i * 4))

# Draw score for Player 0 and 1
print_score()

# Reset the PyGlow and on-board LEDs
pyglow.all(0)
for i in leds:
    GPIO.output(i, False)

# Main loop for a single match (until a point is scored)
# Keeps a stable update rate to ensure the ball travels across the screen in 2 seconds
def match():
    global delta
    global last_time
    global updates
    global timer
    while not check_point_scored():
        now = time.time()
        delta += (now - last_time) / update_freq
        last_time = now
        while delta >= 1:
            delta -= 1
            updates += 1
            # Check if the ball is inside the scores and re-draw if necessary
            print_score_check = False
            if ball_position[0] >= 29 and ball_position[0] <= 31:
                if ball_position[1] >= 2 and ball_position[1] <= 7:
                    print_score_check = True
            elif ball_position[0] >= 48 and ball_position[0] <= 50:
                if ball_position[1] >= 2 and ball_position[1] <= 7:
                    print_score_check = True
            move_and_draw_ball()
            check_wall_collision()
            check_paddle_collision()
            if print_score_check:
                print_score()
            print("Ball Position: " + str(ball_position) + " | Ball Motion: " + str(ball_motion))
        if time.time() - timer > 1:
            print("UPS: " + str(updates))
            timer = time.time()
            updates = 0
        # Check for controller move updates here
        if False:
            pass

# Main game loop:
# Runs while no player has a winning score
while score[0] < 10 and score[1] < 10:
    # Check for button press to serve here, wait if not (wait for input interrupt?)
    if False:
        pass
    serves[player_serve] -= 1
    match()
    # Re-draw the scores
    print_score()
    # PyGlow effects
    for i in range(1, 7):
        pyglow.led([i, i+6, i+12], 255)
        time.sleep(0.5)
    for i in range(6, 0, -1):
        pyglow.led([i, i+6, i+12], 0)
        time.sleep(0.5)
    pyglow.all(0)
    if serves[player_serve] == 0:
        serves[player_serve] = 5
        if player_serve == 0:
            player_serve = 1
        else:
            player_serve = 0
    break
