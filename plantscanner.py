#!/usr/bin/python3

import cv2
from picamera2 import Picamera2
import numpy as np
from trilobot import *
import time
from threading import Thread

# Removed cv2.startWindowThread() as it's not needed without a display server.

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)}))  # OpenCV works in BGR not RGB
picam2.start()

tbot = Trilobot()

speed = 0.5

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


def robot():
    try:
        plants = 0
        while not tbot.read_button(BUTTON_A):
            img = picam2.capture_array()
            distance = tbot.read_distance()

            bgr_thresh = cv2.inRange(img,
                                     np.array((130, 130, 0)),  # lower range
                                     np.array((170, 170, 40)))  # upper range

            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv_thresh = cv2.inRange(hsv_img,
                                     np.array((50, 100, 0)),  # lower range
                                     np.array((80, 255, 255)))  # upper range

            hsv_contours, _ = cv2.findContours(
                hsv_thresh.copy(),
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

            for c in hsv_contours:
                if cv2.contourArea(c) > 100.0:
                    cv2.drawContours(img, c, -1, (255, 0, 0), 10)

            if len(hsv_contours) > 0:
                M = cv2.moments(hsv_contours[0])  # Largest contour
                if M['m00'] > 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    # Removed cv2.circle() and other GUI-related calls since we're running headlessly.

                    if cx < 270:
                        tbot.turn_left(speed)
                        tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW, show=False)
                        tbot.set_underlight(LIGHT_REAR_LEFT, YELLOW, show=True)
                    elif cx >= 370:
                        tbot.turn_right(speed)
                        tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW, show=True)
                        tbot.set_underlight(LIGHT_REAR_LEFT, YELLOW, show=False)
                    elif 370 > cx > 270 and distance > 10:
                        tbot.forward(speed * 2)
                        tbot.set_underlight(LIGHT_REAR_LEFT, GREEN, show=True)
                        tbot.set_underlight(LIGHT_REAR_RIGHT, GREEN, show=True)
                        print(distance)
                    elif 370 > cx > 270 and distance < 10:
                        plants += 1
                        time.sleep(1)
                        tbot.stop()
                        tbot.fill_underlighting(RED)
                        time.sleep(0.1)
                        tbot.fill_underlighting(BLACK)
                        time.sleep(0.1)
                        tbot.fill_underlighting(RED)
                        time.sleep(0.1)
                        tbot.fill_underlighting(BLACK)
                        time.sleep(0.1)
                        tbot.fill_underlighting(RED)
                        time.sleep(2)
                        tbot.turn_left(speed)
                        time.sleep(2)
                        tbot.fill_underlighting(BLACK)
                        tbot.backward(speed)
                        time.sleep(1)
            else:
                print("No Object Found")
                tbot.turn_left(speed)
                tbot.set_underlight(LIGHT_REAR_LEFT, BLUE, show=True)
                tbot.set_underlight(LIGHT_REAR_RIGHT, BLUE, show=True)
    finally:
        tbot.stop()


def main():
    robot_thread = Thread(target=robot)
    robot_thread.daemon = True
    robot_thread.start()
    try:
        robot_thread.join()
    except KeyboardInterrupt:
        tbot.stop()
        print("\nExiting...")


if __name__ == "__main__":
    main()
