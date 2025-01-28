#!/usr/bin/env python3

import time
from trilobot import Trilobot
import sys, termios, tty, os, time

"""
An example of how move Trilobot with keyboard.
# https://www.jonwitts.co.uk/archives/896 #
"""
print("Trilobot Example: Keyboard Movement\n")
print("a = left | w = forward | s = reverse | d = right | x = stop | q = increase speed (0-1) | z = decrease speed (0-1) | p = exit program\n")

tbot = Trilobot()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 
button_delay = 0.2
speed = 0.5

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

LIGHT_FRONT_RIGHT = 0
LIGHT_FRONT_LEFT = 1
LIGHT_MIDDLE_LEFT = 2
LIGHT_REAR_LEFT = 3
LIGHT_REAR_RIGHT = 4
LIGHT_MIDDLE_RIGHT = 5
 
while True:
    char = getch()
 
    if (char == "p"):
        print("Exit")
        exit(0)
 
    if (char == "a"):
        print("Left")
        time.sleep(button_delay)
        tbot.turn_left(speed)
        tbot.set_underlight(LIGHT_FRONT_LEFT, YELLOW, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_LEFT, YELLOW, show=False)
        tbot.set_underlight(LIGHT_REAR_LEFT, YELLOW, show=False)
        tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
        tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
        tbot.show_underlighting()
 
    elif (char == "d"):
        print("Right")
        time.sleep(button_delay)
        tbot.turn_right(speed)
        tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
        tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
        tbot.set_underlight(LIGHT_FRONT_RIGHT, YELLOW, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_RIGHT, YELLOW, show=False)
        tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW, show=False)
        tbot.show_underlighting()
 
    elif (char == "w"):
        print("Forward")
        time.sleep(button_delay)
        tbot.forward(speed)
        tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
        tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
        tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
        tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
        tbot.show_underlighting()
 
    elif (char == "s"):
        print("Reverse")
        time.sleep(button_delay)
        tbot.backward(speed)
        tbot.set_underlight(LIGHT_FRONT_LEFT, RED, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
        tbot.set_underlight(LIGHT_REAR_LEFT, WHITE, show=False)
        tbot.set_underlight(LIGHT_FRONT_RIGHT, RED, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
        tbot.set_underlight(LIGHT_REAR_RIGHT, WHITE, show=False)
        tbot.show_underlighting()
 
    elif (char == "x"):
        print("Stop")
        time.sleep(button_delay)
        tbot.stop()
        tbot.fill_underlighting(RED)
 
    elif (char == "q"):
        print("Increase Speed by 0.1")
        time.sleep(button_delay)
        speed = round(speed + 0.1, 1)
        print("Speed: " + str(speed))
 
    elif (char == "z"):
        print("Decrease Speed by 0.1")
        time.sleep(button_delay)
        speed = round(speed - 0.1, 1)
        print("Speed: " + str(speed))