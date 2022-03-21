#####################################################################

# Task 4 : run a live chroma keying demo using a background image saved
#          as background.jpg

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

camera = cv2.VideoCapture(0)

# define display window

window_name = "Live Camera Input with Chroma Keying Background"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

# set the mouse call back function that will be called every time
# the mouse is clicked inside the display window

cv2.setMouseCallback(window_name, mouse_callback)

#####################################################################

# first, read an image of the new background from file (background.jpg)
# and resize it to be the same size as our camera image

background = cv2.imread('background.jpg', cv2.IMREAD_COLOR)
if background is None:
    print("\nbackground image file not successfully loaded - background.jpg missing!")
    exit(0)
else:
    _, image = camera.read()
    height, width, _ = image.shape
    background = cv2.resize(background, (width, height))

#####################################################################

keep_processing = True

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # convert the RGB images to HSV

    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # create a background mask that identifies the pixels in the range of hues

    background_mask = cv2.inRange(image_HSV, lower_green, upper_green)

    # logically invert the background mask to get the foreground mask using logical NOT

    foreground_mask = cv2.bitwise_not(background_mask)

    # extract the set of contours around the foreground mask and then the
    # largest contour as the foreground object of interest. Update the foreground
    # mask with all the pixels inside this contour

    contours, _ = cv2.findContours(foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) > 0):
        largest_contour = max(contours, key = cv2.contourArea)
        foreground_mask_object = np.zeros((height, width))
        cv2.fillPoly(foreground_mask_object, [largest_contour], (255))

    # recompute the background mask based on the updated foreground mask

    background_mask = ((np.ones((height, width)) * 255) - foreground_mask_object).astype('uint8')

    # cut out the sub-part of the stored background we need using logical AND

    # replacement = cv2.bitwise_and(background, background, mask = background_mask)

    # construct 3-channel RGB feathered masks for blending

    foreground_mask_feathered = cv2.blur(foreground_mask,(15,15)) / 255.0
    background_mask_feathered = cv2.blur(background_mask,(15,15)) / 255.0
    background_mask_feathered = cv2.merge([background_mask_feathered, background_mask_feathered, background_mask_feathered])
    foreground_mask_feathered = cv2.merge([foreground_mask_feathered, foreground_mask_feathered, foreground_mask_feathered])

    # combine current camera image with cloaked region via feathered blending

    choma_key_image = ((background_mask_feathered * background) + (foreground_mask_feathered * image)).astype('uint8')

    # display image with cloaking present

    cv2.imshow(window_name, choma_key_image)

    # start the event loop - if user presses "x" then exit
    # wait 40ms for a key press from the user (i.e. 1000ms / 25 fps = 40 ms)

    key = cv2.waitKey(40) & 0xFF

    if (key == ord('x')):
        keep_processing = False

#####################################################################

# Author : Toby Breckon
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
