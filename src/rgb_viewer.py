#####################################################################

# Task 3 : display live video from an attached camera as RGB channels

#####################################################################

import cv2
import numpy as np

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0)

# define display window

window_name = "Live Camera Input - RGB Channels (left to right - R | G | B)"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

#####################################################################

keep_processing = True

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # construct RGB channel view (N.B. OpenCV is BGR, not RGB channel ordering)

    red = np.zeros(image.shape, dtype=np.uint8)
    red[:, :, 2] = image[:, :, 2]

    green = np.zeros(image.shape, dtype=np.uint8)
    green[:, :, 1] = image[:, :, 1]

    blue = np.zeros(image.shape, dtype=np.uint8)
    blue[:, :, 0] = image[:, :, 0]

    channels = np.hstack((np.hstack((red, green)), blue))

    # display image

    cv2.imshow(window_name, channels)

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

# Author : Toby Breckon, toby.breckon@durham.ac.uk
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
