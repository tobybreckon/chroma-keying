#####################################################################

# Task 2 : identify an image region by hue via point and click

#####################################################################

import cv2
import numpy as np

#####################################################################

# define the range of hues to detect - set automatically using mouse

lower_green = np.uint8(np.array([0, 0, 0]))
upper_green = np.uint8(np.array([255, 255, 255]))

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
              (x, y, ', '.join(str(i) for i in image_hsv[y, x])))

        # set Hue bounds on the Hue with +/- 15 threshold on the range

        upper_green[0] = image_hsv[y, x][0] + 20
        lower_green[0] = image_hsv[y, x][0] - 20

        # set Saturation and Value to eliminate very dark, noisy image regions

        lower_green[1] = 50
        lower_green[2] = 50

    # right button click resets HSV range

    # elif event == cv2.EVENT_RBUTTONDOWN:

    #    lower_green = np.uint8(np.array([0,0,0]))
    #    upper_green = np.uint8(np.array([255,255,255]))


#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0, cv2.CAP_V4L)
1
# define display window

window_name = "Live Camera Input with Selected Hue Region"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

# set the mouse call back function that will be called every time
# the mouse is clicked inside the display window

cv2.setMouseCallback(window_name, mouse_callback)

#####################################################################

keep_processing = True

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # convert the RGB images to HSV

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # create a mask that identifies the pixels in the range of hues

    mask = cv2.inRange(image_hsv, lower_green, upper_green)
    mask_inverted = cv2.bitwise_not(mask)

    # create a grey image and black out the masked area

    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_grey = cv2.bitwise_and(image_grey, image_grey, mask=mask_inverted)

    # black out unmasked area of original image

    image_masked = cv2.bitwise_and(image, image, mask=mask)

    # combine the two images for display

    image_grey = cv2.cvtColor(image_grey, cv2.COLOR_GRAY2BGR)
    image_combined = cv2.add(image_grey, image_masked)

    # display image

    cv2.imshow(window_name, image_combined)

    # start the event loop - if user presses "x" then exit
    # wait 40ms for a key press from the user (i.e. 1000ms / 25 fps = 40 ms)

    key = cv2.waitKey(40) & 0xFF

    if (key == ord('x')):
        keep_processing = False

    # - if user presses "f" then switch to fullscreen

    elif (key == ord('f')):
        print("\n -- toggle fullscreen.")
        last_fs = cv2.getWindowProperty(window_name,
                                        cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN &
                              ~(int(last_fs)))

#####################################################################

# Author : Toby Breckon / Magnus Bordewich
# Copyright (c) 2022-25 Dept Computer Science, Durham University, UK

#####################################################################
