#####################################################################

# Task 2 : identify an image region by hue

#####################################################################

import cv2
import numpy as np

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0)

# define display window

window_name = "HSV - colour selected image"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

#####################################################################

keep_processing = True

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # convert the RGB images to HSV

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # print the HSV values of the middle pixel

    height, width, _ = image.shape
    print('centre pixel HSV value: ', image_hsv[int(height/2)][int(width/2)])
    print()

    # define the range of hues to detect - adjust these to detect different colours

    lower_green = np.array([55, 50, 50])
    upper_green = np.array([95, 255, 255])

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

    # wait 40ms or less for a key press from the user
    # (i.e. 1000ms / 25 fps = 40 ms)

    key = cv2.waitKey(40) & 0xFF

    if (key == ord('x')):
        keep_processing = False

#####################################################################

# Author : Toby Breckon / Magnus Bordewich
# Copyright (c) 2023 Dept Computer Science, Durham University, UK

#####################################################################
