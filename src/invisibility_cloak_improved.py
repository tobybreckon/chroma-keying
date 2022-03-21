#####################################################################

# Task 3 : run an improved live invisibility cloak demo using:
#          (a) a convex hull operation around the foreground
#          (b) feathered blenidng for compositing

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

        lower_green = np.uint8(np.array([255,0,0]))
        upper_green = np.uint8(np.array([255,255,255]))

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(2)

# define display window

window_name = "Live Camera Input with Invisibility Cloaking"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

# set the mouse call back function that will be called every time
# the mouse is clicked inside the display window

cv2.setMouseCallback(window_name, mouse_callback)

#####################################################################

# first, take an image of the background image

_, background = camera.read()
height, width, _ = background.shape
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

    # perform morphological opening and dilation on the foreground mask

    foreground_mask_morphed = cv2.morphologyEx(foreground_mask,
                                cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 5)
    foreground_mask_morphed = cv2.morphologyEx(foreground_mask_morphed,
                                cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations = 5)

    # extract the set of contours around the foreground mask and then the
    # convex hull around that set of contours. Update the foreground mask with
    # the convex hull of all the pixels in the region

    contours, _ = cv2.findContours(foreground_mask_morphed,
                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        hull = cv2.convexHull(np.vstack(list(contours[i] for i in range(len(contours)))))
        cv2.fillPoly(foreground_mask_morphed, [hull], (255,255,255))

    # cut out the sub-part of the stored background we need using logical AND

    cloaking_fill = cv2.bitwise_and(background, background, mask = foreground_mask_morphed)

    # construct 3-channel RGB feathered background mask for blending

    foreground_mask_feathered = cv2.GaussianBlur(foreground_mask_morphed,(15,15),0) / 255.0
    background_mask_feathered = np.ones((height, width)) - (foreground_mask_morphed / 255.0)
    background_mask_feathered = cv2.merge([background_mask_feathered, background_mask_feathered, background_mask_feathered])

    # combine current camera image with cloaked region via feathered blending

    cloaked_image = ((background_mask_feathered * image) + (cloaking_fill)).astype('uint8')

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

# Author : Toby Breckon
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
