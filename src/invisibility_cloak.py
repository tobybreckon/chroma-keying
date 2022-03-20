#####################################################################

# Task 3 : run a live invisibility cloak demo

#####################################################################

import cv2
import numpy as np

#####################################################################

# define the range of hues to detect - set automatically using mouse

lower_green = np.uint8(np.array([255,0,0]))
upper_green = np.uint8(np.array([255,255,255]))

#####################################################################

# mouse callback function - activated on any mouse event (click, movement)
# displays and sets Hue range based on right click location

def mouse_callback(event, x, y, flags, param):

    global upper_green
    global lower_green

    # records mouse events at postion (x,y) in the image window

    # left button click prints colour HSV information and sets range

    if event == cv2.EVENT_LBUTTONDOWN:
        print("HSV colour @ position (%d,%d) = %s (bounds set with +/- 20)" %
              (x, y, ', '.join(str(i) for i in image_HSV[y, x])))

        # set Hue bounds on the Hue with +/- 15 threshold on the range

        upper_green[0] = image_HSV[y, x][0] + 20
        lower_green[0] = image_HSV[y, x][0] - 20

        # set Saturation and Value to eliminate very dark, noisy image regions

        lower_green[1] = 50
        lower_green[2] = 50

    # right button click resets HSV range

    elif event == cv2.EVENT_RBUTTONDOWN:

        lower_green = np.uint8(np.array([0,0,0]))
        upper_green = np.uint8(np.array([255,255,255]))

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(2)

# define display window

window_name = "Live Camera Input with Invisibility Cloaking"
cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)

# set the mouse call back function that will be called every time
# the mouse is clicked inside the display window

cv2.setMouseCallback(window_name, mouse_callback)

#####################################################################

# first, take an image of the background image

_, background = camera.read()
cv2.imshow("Current Background", background)

#####################################################################

keep_processing = True

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # convert the RGB images to HSV

    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # create a foreground mask that identifies the pixels in the range of hues

    foreground_mask = cv2.inRange(image_HSV, lower_green, upper_green)

    # logically invert the foreground mask to get the background mask using logical NOT

    background_mask = cv2.bitwise_not(foreground_mask)

    # perform morphological opening and dilation on the foreground mask

    foreground_mask_morphed = cv2.morphologyEx(foreground_mask,
                                cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 5)
    foreground_mask_morphed = cv2.morphologyEx(foreground_mask_morphed,
                                cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations = 5)

    # cut out the sub-part of the stored background we need using logical AND

    cloaking_fill = cv2.bitwise_and(background, background, mask = foreground_mask_morphed)

    # cut out the sub-part of the camera image we need using logical AND

    current_background = cv2.bitwise_and(image, image, mask = background_mask)

    # combine both using logical OR

    cloaked_image = cv2.bitwise_or(current_background, cloaking_fill)

    # display image with cloaking present

    cv2.imshow(window_name, cloaked_image)

    # start the event loop - if user presses "x" then exit
    # wait 40ms for a key press from the user (i.e. 1000ms / 25 fps = 40 ms)

    key = cv2.waitKey(40) & 0xFF

    if (key == ord('x')):
        keep_processing = False

    # - if user presses space then reset background

    elif (key == ord(' ')):
        print("\n -- reset of background image.")
        _, background = camera.read()
        cv2.imshow("Current Background", background)

#####################################################################

# Author : Toby Breckon / Chris Willcocks
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
