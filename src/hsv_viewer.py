#####################################################################

# Task 3 : display live video from an attached camera as HSV channels

#####################################################################

import cv2
import numpy as np

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0, cv2.CAP_V4L)

# define display window

window_name = "Live Camera Input - HSV Channels (left to right - H | S | V)"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

#####################################################################

keep_processing = True

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # construct HSV channel view (with colour mapped Hue)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hue = np.zeros(image_hsv.shape, dtype=np.uint8)
    hue[:, :, 0] = np.uint8(image_hsv[:, :, 0] * (0.7))
    hue[:, :, 1] = np.ones(image_hsv[:, :, 1].shape) * 255
    hue[:, :, 2] = np.ones(image_hsv[:, :, 2].shape) * 255
    colour_mapped_hue = cv2.cvtColor(hue, cv2.COLOR_HSV2RGB)  # RGB better

    saturation = cv2.cvtColor(image_hsv[:, :, 1], cv2.COLOR_GRAY2BGR)
    value = cv2.cvtColor(image_hsv[:, :, 2], cv2.COLOR_GRAY2BGR)

    channels = np.hstack((np.hstack((colour_mapped_hue, saturation)), value))

    # display image

    cv2.imshow(window_name, channels)

    # start the event loop - if user presses "x" or ESC then exit
    # wait 40ms for a key press from the user (i.e. 1000ms / 25 fps = 40 ms)

    key = cv2.waitKey(40) & 0xFF

    if (key == ord('x') or key == ord('\x1b')):
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

# Author : Toby Breckon
# Copyright (c) 2022-25 Dept Computer Science, Durham University, UK

#####################################################################
