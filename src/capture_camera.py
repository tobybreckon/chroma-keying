#####################################################################

# Task 1 : capture live video from an attached camera

#####################################################################

import cv2

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0, cv2.CAP_V4L)

# define display window

window_name = "Live Camera Input"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

#####################################################################

keep_processing = True

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # optional flip (1 = left/right; 0 = top/bottom; -1 = both)

    # image = cv2.flip(image, -1)

    # optional image blurring

    # image = cv2.GaussianBlur(image, (15, 15), 0)

    # display image

    cv2.imshow(window_name, image)

    # start the event loop - if user presses "x" or ESC then exit

    # wait 40ms or less for a key press from the user
    # (i.e. 1000ms / 25 fps = 40 ms)

    key = cv2.waitKey(40) & 0xFF

    if (key == ord('x') or key == ord('\x1b')):
        keep_processing = False

#####################################################################

# Author : Toby Breckon
# Copyright (c) 2022-25 Dept Computer Science, Durham University, UK

#####################################################################
