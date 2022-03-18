#####################################################################

# Task 1 : capture live video from an attached camera

#####################################################################

import cv2
import math


#####################################################################

keep_processing = True

#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass


#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0)

# define display window

window_name = "Live Camera Input with Blurring"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# add some track bar GUI controllers for smoothing filter parameters

smoothing_neighbourhood_x = 3
cv2.createTrackbar(
    "filter size - X",
    window_name,
    smoothing_neighbourhood_x,
    250,
    nothing)

smoothing_neighbourhood_y = 3
cv2.createTrackbar(
    "filter size - Y",
    window_name,
    smoothing_neighbourhood_y,
    250,
    nothing)

#####################################################################

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # start a timer (to see how long processing and display takes)

    start_t = cv2.getTickCount()

    # get parameters from track bars

    smoothing_neighbourhood_x = cv2.getTrackbarPos("filter size - X",
                                                 window_name)
    smoothing_neighbourhood_y = cv2.getTrackbarPos("filter size - Y",
                                                 window_name)

    # check filter sizes are greater than 3 and odd

    smoothing_neighbourhood_x = max(3, smoothing_neighbourhood_x)
    if not(smoothing_neighbourhood_x % 2):
        smoothing_neighbourhood_x = smoothing_neighbourhood_x + 1

    smoothing_neighbourhood_y = max(3, smoothing_neighbourhood_y)
    if not(smoothing_neighbourhood_y % 2):
        smoothing_neighbourhood_y = smoothing_neighbourhood_y + 1

    # performing smoothing on the image using a smoothing filter

    smoothed_image = cv2.GaussianBlur(image, (smoothing_neighbourhood_x,
                                smoothing_neighbourhood_y), 0)

    # stop the timer and convert to milliseconds
    # (to see how long processing and display takes)

    stop_t = ((cv2.getTickCount() - start_t) /
              cv2.getTickFrequency()) * 1000

    label = ('Processing time: %.2f ms' % stop_t) + \
        (' (Max Frames per Second (fps): %.2f' % (1000 / stop_t)) + ')'
    cv2.putText(smoothed_image, label, (0, 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    # display image

    cv2.imshow(window_name, smoothed_image)

    # start the event loop - if user presses "x" then exit

    # wait 40ms or less for a key press from the user
    # depending on processing time taken (i.e. 1000ms / 25 fps = 40 ms)

    key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF


    if (key == ord('x')):
        keep_processing = False

#####################################################################

# Author : Toby Breckon, toby.breckon@durham.ac.uk
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
