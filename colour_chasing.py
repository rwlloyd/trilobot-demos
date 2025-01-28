#!/usr/bin/python3

import cv2
from picamera2 import Picamera2
import numpy as np
from trilobot import Trilobot

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)})) # opencv works in BGR not RGB
picam2.start()

tbot = Trilobot()

speed = 0.4

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

while True:
    img = picam2.capture_array()

    # using the BGR colour space, create a mask for everything that is in a certain range
    bgr_thresh = cv2.inRange(img,
                                np.array((130, 130, 0)), # lower range
                                np.array((170, 170, 40))) # upper range

    # It often is better to use another colour space, that is less sensitive to illumination (brightness) changes.
    # The HSV colour space is often a good choice. 
    # So, we first change the colour space here...
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a binary (mask) image, HSV = hue (colour) (0-180), saturation  (0-255), value (brightness) (0-255)
    hsv_thresh = cv2.inRange(hsv_img,
                                np.array((50, 100, 0)), # lower range
                                np.array((80, 255, 255))) # upper range

    # just for the fun of it, print the mean value of each HSV channel within the mask 
    # print(cv2.mean(hsv_img[:, :, 0], mask = hsv_thresh)[0])
    # print(cv2.mean(hsv_img[:, :, 1], mask = hsv_thresh)[0])
    # print(cv2.mean(hsv_img[:, :, 2], mask = hsv_thresh)[0])

    # This is how we could find actual contours in the BGR image, but we won't do this now.
    # _, bgr_contours, hierachy = cv2.findContours(
    #     bgr_thresh.copy(),
    #     cv2.RETR_TREE,
    #     cv2.CHAIN_APPROX_SIMPLE)

    # Instead find the contours in the mask generated from the HSV image.
    hsv_contours, hierachy = cv2.findContours(
        hsv_thresh.copy(),
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    
    # in hsv_contours we now have an array of individual closed contours (basically a polgon around the blobs in the mask). Let's iterate over all those found contours.
    for c in hsv_contours:
        # This allows to compute the area (in pixels) of a contour
        a = cv2.contourArea(c)
        # and if the area is big enough, we draw the outline
        # of the contour (in blue)
        if a > 100.0:
            cv2.drawContours(img, c, -1, (255, 0, 0), 10)
    #print('====')

    # if there are contours drive the robot left and right to center on the largest contour
    if len(hsv_contours) > 0:
            # find the centre of the contour: https://docs.opencv.org/3.4/d8/d23/classcv_1_1Moments.html
            M = cv2.moments(hsv_contours[0]) # only select the largest controur
            if M['m00'] > 0:
                # find the centroid of the contour
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                #print("Centroid of the biggest area: ({}, {})".format(cx, cy))

                # Draw a circle centered at centroid coordinates
                # cv2.circle(image, center_coordinates, radius, color, thickness) -1 px will fill the circle
                cv2.circle(img, (round(cx), round(cy)), 50, (0, 255, 0), -1)
                            
                # find height/width of robot camera image from ros2 topic echo /camera/image_raw height: 1080 width: 1920

                # if center of object is to the left of image center move left
                if cx < 270:                   
                    tbot.turn_left(speed)
                    tbot.fill_underlighting(YELLOW)
                # else if center of object is to the right of image center move right
                elif cx >= 370:                    
                    tbot.turn_right(speed)
                    tbot.fill_underlighting(YELLOW)
                else: # center of object is in a 100 px range in the center of the image so dont turn
                    #print("object in the center of image")                    
                    tbot.stop()
                    tbot.fill_underlighting(GREEN)
                    
    else:
        print("No Object Found")
        # turn until we can see a coloured object
        tbot.turn_left(speed)
        tbot.fill_underlighting(RED)


    #img_small = cv2.resize(img, (0,0), fx=0.4, fy=0.4) # reduce image size
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert back to rgb image
    cv2.imshow("Image window", img)
    cv2.waitKey(1)