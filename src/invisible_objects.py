#####################################################################

# Task 5 : run a machine learning based invisibility cloak demo using:
#          (a) trained object detection for person detection
#          (b) feathered blenidng for compositing (as before)

#####################################################################

import cv2
import numpy as np

#####################################################################

# define video capture with access to camera 0

camera = cv2.VideoCapture(0)

# define display window

window_name = "Live Camera Input with Invisibility Cloaking"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

#####################################################################

# first, take an image of the background image

_, background = camera.read()
height, width, _ = background.shape
cv2.imshow("Current Background", background)

##########################################################################

# initialise the object detection neural network (uses Mask R-CNN)

# load configuration and weight files for the Mask R-CNN model

net = cv2.dnn.readNet("mask_rcnn_inception_v2_coco_2018_01_28.pbtxt",
                      "mask_rcnn_inception_v2_coco_2018_01_28/"
                      + "/frozen_inference_graph.pb")

# load names of object classes (types) from file

classesFile = "object_detection_classes_coco.txt"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# set up compute target as one of [GPU, OpenCL, CPU] - uncomment as needed

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#####################################################################

# set up an array of colours in order to draw detected object masks

np.random.seed(324)
colors = [np.array([0, 0, 0], np.uint8)]
for i in range(1, len(classes) + 1):
    colors.append((colors[i - 1] +
                   np.random.randint(0, 256, [3],
                   np.uint8)) / 2
                  )
del colors[0]

#####################################################################

# main processing loop

keep_processing = True
do_invisibility = False

while (keep_processing):

    # read an image from the camera

    _, image = camera.read()

    # get image dimensions

    height = image.shape[0]
    width = image.shape[1]

    # set up a foreground mask image (all zeros == black)

    foreground_mask = np.zeros((height, width, 1), np.uint8)

    # create a 4D tensor (OpenCV 'blob') from image frame
    # (N.B. technical aspect: pixels not scaled, image resized)
    tensor = cv2.dnn.blobFromImage(
                image, 1.0, (800, 800), [0, 0, 0],
                swapRB=True, crop=False)

    # set the input to the CNN network
    net.setInput(tensor)

    # runs forward inference to get object masks from final output layer
    boxes, masks = net.forward(['detection_out_final', 'detection_masks'])

    # get number of objects detected
    numDetections = boxes.shape[2]

    # draw segmentation - draw instance segments

    boxesToDraw = []
    for i in range(numDetections):
        box = boxes[0, 0, i]
        mask = masks[i]
        confidence = box[2]
        if confidence > 0.5:

            # **** get object info: type, bounding box

            classId = int(box[1])
            left = int(width * box[3])
            top = int(height * box[4])
            right = int(width * box[5])
            bottom = int(height * box[6])

            # **** check bounding box inside the image width/height

            left = max(0, min(left, width - 1))
            top = max(0, min(top, height - 1))
            right = max(0, min(right, width - 1))
            bottom = max(0, min(bottom, height - 1))

            # **** draw object instance mask

            # get mask, re-size from 28x28 network output
            # to size of bounding box size in image then theshold mask at 0.5

            classMask = mask[classId]
            classMask = cv2.resize(classMask,
                                   (right - left + 1, bottom - top + 1),
                                   cv2.INTER_CUBIC)
            mask = (classMask > 0.5)

            roi = image[top:bottom+1, left:right+1][mask]

            # if invisibility is ON, draw objects into foreground mask
            # otherwise draw them as coloured overlays on the camera image

            if (do_invisibility):
                foreground_mask[top:bottom+1, left:right+1][mask] = 255
            else:
                image[top:bottom+1, left:right+1][mask] = (
                    0.8 * colors[classId] + 0.2 * roi).astype(np.uint8)

    if (do_invisibility):

        # all as per earlier Task 3 and Task 4 code

        # perform morphological opening and dilation on the foreground mask

        foreground_mask_morphed = cv2.morphologyEx(foreground_mask,
                                                   cv2.MORPH_OPEN,
                                                   np.ones((3, 3), np.uint8),
                                                   iterations=5)
        foreground_mask_morphed = cv2.morphologyEx(foreground_mask_morphed,
                                                   cv2.MORPH_DILATE,
                                                   np.ones((3, 3), np.uint8),
                                                   iterations=5)

        # extract the set of contours around the foreground mask and then the
        # convex hull around that set of contours. Update the foreground mask
        # with the convex hull of all the pixels in the region

        contours, _ = cv2.findContours(foreground_mask_morphed,
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        if (len(contours) > 0):
            hull = cv2.convexHull(np.vstack(list(contours[i]
                                            for i in range(len(contours)))))
            cv2.fillPoly(foreground_mask_morphed, [hull], (255, 255, 255))

        # logically invert foreground mask to get the background mask via NOT

        background_mask = cv2.bitwise_not(foreground_mask_morphed)

        # cut out sub-part of the stored background we need using logical AND

        cloaking_fill = cv2.bitwise_and(background, background,
                                        mask=foreground_mask_morphed)

        # construct 3-channel RGB feathered background mask for blending

        foreground_mask_feathered = cv2.blur(foreground_mask_morphed,
                                             (15, 15)) / 255.0
        background_mask_feathered = cv2.blur(background_mask, (15, 15)) / 255.0
        background_mask_feathered = cv2.merge([background_mask_feathered,
                                               background_mask_feathered,
                                               background_mask_feathered])
        foreground_mask_feathered = cv2.merge([foreground_mask_feathered,
                                               foreground_mask_feathered,
                                               foreground_mask_feathered])

        # combine current image with cloaked region via feathered blending

        cloaked_image = ((background_mask_feathered * image) +
                         (foreground_mask_feathered * background)
                         ).astype('uint8')

        # display image with cloaking present

        cv2.imshow(window_name, cloaked_image)

    else:

        # display image with just object masks present

        cv2.imshow(window_name, image)

    # start the event loop - if user presses "x" then exit
    # wait just 2ms for a key press (as processsing here is slower)

    key = cv2.waitKey(2) & 0xFF

    if (key == ord('x')):
        keep_processing = False

    # - if user presses 'i' then turn on/off invisibility

    elif (key == ord('i')):

        do_invisibility = not(do_invisibility)

    # - if user presses space then reset background

    elif (key == ord(' ')):
        print("\n -- reset of background image.")
        _, background = camera.read()
        cv2.imshow("Current Background", background)

#####################################################################

# Author : Toby Breckon
# Copyright (c) 2022 Dept Computer Science, Durham University, UK

#####################################################################
