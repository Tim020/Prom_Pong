from serial import Serial
from services import *
from audio import Audio
from PyGlow import PyGlow
from math import floor
import time
import random
import threading
import RPi.GPIO as GPIO

debug = False

# Size of the window
window_size = [80, 40]
# Number of serves each player has
serves = [5, 5]
# Current score of each player
score = [0, 0]
# Size of the player's bats
default_bat_size = 3
bat_size = [default_bat_size, default_bat_size]
# Big things left
power_ups = [2, 2]
# Top position of the bat for each player (initially in the middle)
bat_position = [(window_size[1] - bat_size[0]) / 2, (window_size[1] - bat_size[0]) / 2]
# How wide the voltage range is for each possible bat_position
#   1538 Comes from the range of values the ADC can give us between 0.5V and 2.5V
voltage_range = 1538 / ((window_size[1] - default_bat_size) + 1)
# Ball position
ball_position = [4, window_size[1] / 2]
# Ball motion
ball_motion = [0, 0]
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
# Has the player served?
serve = [False, False]
# Different timings for the ball to travel across the screen
ball_speeds = [float(10), float(10), float(5), float(15)]

update_freq = ball_speeds[0] / window_size[0]
delta = 0
last_time = 0
timer = 0
updates = 0
i2c = I2C()


# Used when sending commands to the serial port, send to the console if in a dev environment (ie not on a Pi)
def output(seq):
    if debug:
        pass
    else:
        serialPort.write(seq)


def update_bat_pos(player):
    """
    Update the bat positions for both players
    :param player: 0 or 1 for player 1 or 2 respectively
    """
    global bat_position
    if player == 0:
        channel = 1
    elif player == 1:
        channel = 2
    else:
        raise ValueError("player param must be 0 or 1")
    player_input = i2c.get_adc_value(channel)
    new_pos = floor(player_input / voltage_range) + 1

    # If the bat has only moved only into the position next to it, check that it has moved in quite a bit
    # Works sort of like a Schmitt trigger
    if new_pos == bat_position[player] + 1:
        if player_input > ((new_pos - 1) * voltage_range) + (voltage_range / 32):
            new_pos = bat_position[player]
    elif new_pos == bat_position[player] - 1:
        if player_input < (new_pos * voltage_range) - (voltage_range / 32):
            new_pos = bat_position[player]

    # Check whether the bottom of the bat is within the screen, if not move it up
    bottom_space = window_size[1] - (new_pos + bat_size[player] - 1)
    if bottom_space < 0:
        new_pos += bottom_space

    # Update the position
    if new_pos != bat_position[player]:
        # Work out the x-position to draw the bat at
        if player == 0:
            start_x = 3
        else:
            start_x = window_size[0] - 2
        # Un-draw the current bat
        output(ANSIEscape.undraw_bat(start_x, bat_position[player], bat_size[player]))
        # Update the bat position
        bat_position[player] = new_pos
        # Redraw the new bat
        output(ANSIEscape.draw_bat(start_x, bat_position[player], bat_size[player]))


# Un-draw and re-draw the players scores
def print_score():
    global score
    # Set the colour to green
    output("\033[42m")
    # Clear the area the scores are drawn in
    for y in range(0, 5):
        output(ANSIEscape.set_cursor_position(29, 2 + y))
        output(" " * 3)
    for y in range(0, 5):
        output(ANSIEscape.set_cursor_position(48, 2 + y))
        output(" " * 3)
    # Print the two scores
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
        output("\033[47m")  # White
    else:
        output("\033[42m")  # Green
    output(" ")

    # Update the ball position
    ball_position[0] += ball_motion[0]
    ball_position[1] += ball_motion[1]

    # Update the on board LED
    GPIO.output(leds[active_led], False)
    active_led = ball_position[0] / led_steps
    GPIO.output(leds[active_led], True)

    # Finally draw the new ball
    output(ANSIEscape.set_cursor_position(ball_position[0], ball_position[1]))
    output("\033[43m")
    output(" ")


def move_and_draw_ball_serve():
    global ball_position
    global player_serve
    global bat_position

    # Centre the ball on the serving players paddle
    new_pos = bat_position[player_serve] + 2
    # If the ball has moved, un-draw and redraw it
    if ball_position[1] != new_pos:
        # Move the cursor to the correct position, set the background colour and un-draw the ball
        output(ANSIEscape.set_cursor_position(ball_position[0], ball_position[1]))
        output("\033[42m")
        output(" ")
        # Move the cursor to the correct position, set the background colour and re-draw the ball
        ball_position[1] = new_pos
        output(ANSIEscape.set_cursor_position(ball_position[0], ball_position[1]))
        output("\033[43m")
        output(" ")


# Checks if the ball has hit the top or bottom edge and updates the motion as appropriate
def check_wall_collision():
    global ball_position
    global window_size
    global ball_motion
    # Is the ball at the top or bottom edge (ignore x position)
    if ball_position[1] == 1 or ball_position[1] == window_size[1]:
        # Check if the ball is rolling along the wall edge, give it some motion if it is
        if ball_motion[1] == 0:
            if ball_position[1] == 1:
                ball_motion[1] = -1
            elif ball_position[1] == window_size[1]:
                ball_motion[1] = 1
        else:
            ball_motion[1] *= -1


# Checks if the ball has hit a paddle and updates the motion as appropriate
# TODO: make the rebound direction depend on where on the paddle the ball has hit, maybe decrease default bat size to 3?
def check_paddle_collision():
    global ball_position
    global bat_position
    global bat_size
    global ball_motion
    global update_freq
    if ball_position[0] == 4:
        if bat_position[0] <= ball_position[1] <= bat_position[0] + bat_size[0]:
            divisions = bat_size[0] // 3
            dY = ball_position[1] - bat_position[0]
            if dY <= bat_position[0] + divisions:
                ball_motion[1] = 1
            elif dY <= bat_position[0] + 2 * divisions:
                ball_motion[1] = 0
            elif dY <= bat_position[0] + 2 * divisions:
                ball_motion[1] = -1
            ball_motion[1] = random.choice([-1, -1, 0, 1, 1])
            update_freq = random.choice(ball_speeds) / window_size[0]
            audio.tone1(0.2)
    elif ball_position[0] == window_size[0] - 3:
        if bat_position[1] <= ball_position[1] <= bat_position[1] + bat_size[1]:
            divisions = bat_size[0] // 3
            dY = ball_position[1] - bat_position[0]
            if dY <= bat_position[1] + divisions:
                ball_motion[1] = 1
            elif dY <= bat_position[1] + 2 * divisions:
                ball_motion[1] = 0
            elif dY <= bat_position[1] + 2 * divisions:
                ball_motion[1] = -1
            ball_motion[0] *= -1
            update_freq = random.choice(ball_speeds) / window_size[0]
            audio.tone1(0.2)


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


def set_serve_p1():
    global serve
    print "Setting P1 serve"
    serve[0] = True


def set_serve_p2():
    global serve
    print "Setting P2 serve"
    serve[1] = True


def set_power_up_p1():
    global bat_size
    global power_ups
    global default_bat_size
    if power_ups[0] > 0 and bat_size[0] == default_bat_size:
        print "Setting P1 power up"
        power_ups[0] -= 1
        output(ANSIEscape.undraw_bat(3, bat_position[0], bat_size[0]))
        bat_size[0] = default_bat_size * 2
        output(ANSIEscape.draw_bat(3, bat_position[0], bat_size[0]))
        threading.Timer(15, reset_power_up_p1).start()


def set_power_up_p2():
    global bat_size
    global power_ups
    global default_bat_size
    if power_ups[1] > 0 and bat_size[1] == default_bat_size:
        print "Setting P2 power up"
        power_ups[1] -= 1
        output(ANSIEscape.undraw_bat(window_size[0] - 2, bat_position[1], bat_size[1]))
        bat_size[1] = default_bat_size * 2
        output(ANSIEscape.draw_bat(window_size[0] - 2, bat_position[1], bat_size[1]))
        threading.Timer(15, reset_power_up_p2).start()


def reset_power_up_p1():
    global bat_size
    global default_bat_size
    output(ANSIEscape.undraw_bat(3, bat_position[0], bat_size[0]))
    bat_size[0] = default_bat_size
    output(ANSIEscape.draw_bat(3, bat_position[0], bat_size[0]))


def reset_power_up_p2():
    global bat_size
    global default_bat_size
    output(ANSIEscape.undraw_bat(window_size[0] - 2, bat_position[1], bat_size[1]))
    bat_size[1] = default_bat_size
    output(ANSIEscape.draw_bat(window_size[0] - 2, bat_position[1], bat_size[1]))


# Test code to see whether we are running properly on the Pi or not, opens the serial connection if we are
if not debug:
    # Open Pi serial port, speed 115200 bits per second
    serialPort = Serial("/dev/ttyAMA0", 115200)

    # Should not need, but just in case
    if not serialPort.isOpen():
        serialPort.open()

    # Set up the PyGlow module
    pyglow = PyGlow()

    # Set up the RPi.GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Enable the LEDs for the bat position
    for i in leds:
        GPIO.setup(i, GPIO.OUT)

    # Enable the pins for the serve and power-up buttons
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(9, GPIO.IN)
    GPIO.setup(10, GPIO.IN)
    GPIO.setup(11, GPIO.IN)

    # Create the audio object
    audio = Audio()

# Play intro music
audio.play_intro_music()

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
output(ANSIEscape.draw_bat(3, bat_position[0], bat_size[0]))
output(ANSIEscape.draw_bat(window_size[0] - 2, bat_position[1], bat_size[1]))

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

# Set up button listeners for players
p1_serve = ButtonListener(9, GPIO.FALLING, set_serve_p1)
p2_serve = ButtonListener(10, GPIO.FALLING, set_serve_p2)
p1_power = PollingButtonListener(i2c.get_adc_gpio, set_power_up_p1)
p2_power = ButtonListener(11, GPIO.FALLING, set_power_up_p2)


# Main loop for a single match (until a point is scored)
# Keeps a stable update rate to ensure the ball travels across the screen in 2 seconds
def match():
    global delta
    global last_time
    global updates
    global timer
    global ball_position
    global bat_position

    # Timing control initialisation
    last_time = time.time()
    timer = time.time()

    move_and_draw_ball()
    while not check_point_scored():
        # Timing control loop
        now = time.time()
        delta += (now - last_time) / update_freq
        last_time = now

        # Update the position of the two bats
        update_bat_pos(0)
        update_bat_pos(1)

        # If there has been enough time elapsed to update the ball, do so
        while delta >= 1:
            # Reset the time difference and increase the update count
            delta -= 1
            updates += 1

            # Check if the ball is inside the scores and re-draw if necessary
            print_score_check = False
            if 29 <= ball_position[0] <= 31:
                if 2 <= ball_position[1] <= 7:
                    print_score_check = True
            elif 48 <= ball_position[0] <= 50:
                if 2 <= ball_position[1] <= 7:
                    print_score_check = True

            # Logic to move ball and check for collisions
            move_and_draw_ball()
            check_wall_collision()
            check_paddle_collision()

            # Draw the score again if the ball has gone through it
            if print_score_check:
                print_score()

        if time.time() - timer > 1:
            timer = time.time()
            print "UPS: {}".format(updates)
            updates = 0


# Main game loop, runs while no player has a winning score
while score[0] < 10 and score[1] < 10:
    # Undraw the ball
    output(ANSIEscape.set_cursor_position(ball_position[0], ball_position[1]))
    output("\033[42m")
    output(" ")
    # Align the X position of the ball to be on the edge of the serving player's paddle
    if player_serve == 0:
        ball_position[0] = 4
    else:
        ball_position[0] = window_size[0] - 3

    # Zero ball motion before the start of each game
    ball_motion[0] = 0
    ball_motion[1] = 0

    # Wait for button press to serve here, until that time still allow the paddles to move and update them accordingly
    while not serve[player_serve]:
        update_bat_pos(0)
        update_bat_pos(1)
        move_and_draw_ball_serve()

    audio.tone1(0.4)
    # Player has served, decrease the serves left
    serves[player_serve] -= 1

    # Set the initial motion of the ball
    if player_serve == 0:
        ball_motion[0] = 1
    else:
        ball_motion[0] = -1
    ball_motion[1] = random.choice([-1, -1, 0, 1, 1])

    # Start the match
    match()
    audio.tone2(0.4)

    # Reset the serve button
    serve[player_serve] = False

    # Re-draw the scores
    print_score()

    # PyGlow effects for point scored
    for i in range(1, 7):
        pyglow.led([i, i + 6, i + 12], 255)
        time.sleep(0.5)
    for i in range(6, 0, -1):
        pyglow.led([i, i + 6, i + 12], 0)
        time.sleep(0.5)
    pyglow.all(0)

    # Change serving player if current one has no serves left
    if serves[player_serve] == 0:
        serves[player_serve] = 5
        if player_serve == 0:
            player_serve = 1
        else:
            player_serve = 0

# TODO: Clear screen and print winner or something
