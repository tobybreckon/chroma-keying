#####################################################################

# Task 1 : capture an image from an attached camera

#####################################################################

import cv2

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0)

# read an image from the camera

_, image = camera.read()

# perform any processing on the image here
# by uncommenting (remove #) one or both of the following lines

# cv2.flip(image,-1)
# image = cv2.GaussianBlur(image,(5,5),0)

# display the image in the window

cv2.imshow("Live Camera Input", image)

# wait indefinitely for any key press to exist

cv2.waitKey(0)

#####################################################################

# Author : Toby Breckon, toby.breckon@durham.ac.uk
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
