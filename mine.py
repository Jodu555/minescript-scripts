import sys
import time
import minescript

# Usage:
# \mine 11 500
#
# width = horizontal length of each pass
# rows  = number of passes

WIDTH = int(sys.argv[1]) if len(sys.argv) > 1 else 11
ROWS = int(sys.argv[2]) if len(sys.argv) > 2 else 500

# Seconds required to move one block.
# Adjust for your movement speed.
BLOCK_TIME = 0.22

LOOK_PITCH = -90  # straight up
TURN_DELAY = 0.20

yaw, _ = minescript.player_orientation()

# Face straight up
minescript.player_set_orientation(180, LOOK_PITCH)

# Hold left click for entire run
try:
    minescript.player_press_attack(True)
except AttributeError:
    # Older versions may use a generic key function
    minescript.player_press_key("key.attack", True)


def move_left(blocks):
    minescript.player_press_left(True)
    time.sleep(blocks * BLOCK_TIME)
    minescript.player_press_left(False)


def move_right(blocks):
    minescript.player_press_right(True)
    time.sleep(blocks * BLOCK_TIME)
    minescript.player_press_right(False)


def move_forward(blocks):
    minescript.player_press_forward(True)
    time.sleep(blocks * BLOCK_TIME)
    minescript.player_press_forward(False)


try:
    for row in range(ROWS):

        if row % 2 == 0:
            move_right(WIDTH)
        else:
            move_left(WIDTH)

        # Don't advance after the final row
        if row != ROWS - 1:
            move_forward(1)
            time.sleep(TURN_DELAY)

finally:
    try:
        minescript.player_press_attack(False)
    except AttributeError:
        minescript.player_press_key("key.attack", False)

    minescript.player_press_forward(False)
    minescript.player_press_left(False)
    minescript.player_press_right(False)
