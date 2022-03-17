#####################################################################

# Task 1 : capture an image from an attached camera

#####################################################################

import cv2

#####################################################################

# define video capture with access to camera 0

cap = cv2.VideoCapture(0)

# read an image from the camera

_, frame = cap.read()

# display the image in the window

cv2.imshow("Live Camera Input", frame)

# wait indefinitely for any key press to exist

cv2.waitKey(0)


#####################################################################
