#####################################################################

# Task 2 : identify an image region by hue

#####################################################################

import cv2
import numpy as np

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0)

# read an image from the camera

_, image = camera.read()

# convert the RGB images to HSV

image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# print the HSV values of the middle pixel

height, width, _ = image.shape
print('Middle pixel HSV: ', image_hsv[int(height/2)][int(width/2)])

# define the range of hues to detect - adjust these to detect different colours

lower_green = np.array([75, 50, 50])
upper_green = np.array([100, 255, 255])

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

# display the image in the window

cv2.imshow("HSV - colour selected image", image_combined)

# wait indefinitely for any key press to exist

cv2.waitKey(0)

#####################################################################

# Author : Toby Breckon / Magnus Bordewich
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
