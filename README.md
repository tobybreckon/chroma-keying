# Colour Selection and Filtering in Real-time Video

This repository contains a set of computer science taster coding excercises for colour filtering from a live video image, including Harry Potter style invisibility cloaking. It is designed to give you a starter experience in Python coding and real-time image manipuluation.

## Getting Started

Four quick steps to get you started:

1. Ensure the computer is booted into Linux
2.  Login with the provided username and password
3.  Start Visual Studio Code (Menu: Applications > Programming > Visual Studio Code)
4.  Within Visual Studio Code select menu item: File > New File
    * Click _"Selection a language"_ and choose _"Python"_
    * It will then say _"Do you want to install the recommended extensions for Python?"_
    * Click _"Install"_ and wait ~1 minute whilst everything is setup for you

**You are now ready to start coding** - make sure you have all the supporting materials to hand, and go to **Task 1**

#### Supporting Materials

_[ All supplied if you doing this as a visitor to [Computer Science at Durham University](https://www.durham.ac.uk/departments/academic/computer-science/) ]_

- a Linux PC with [OpenCV](https://www.opencv.org) and [Visual Studio Code](https://code.visualstudio.com/) installed
- 1 x USB webcam (that works under Linux with the UVC driver)
- 1 x green covered chroma-keying material

## Task 1 - Capture a Live Camera Image

Once you have completed the **Getting Started** steps:

- copy and paste the code from this example [capture_camera.py](capture_camera.py) into your Visual Studio Code window
- save this file as ```main.py``` by selecting menu item: File > Save As... > main.py
10) Click "Run > Run Without Debugging", you should see a black window


those elements installed you can obtain an openCV image object with the python program <a href="https://github.com/MagnusBordewich/ObjectTracking/blob/master/RaspberryPi/1-capture_image.py">1-capture_image.py</a>. Open it in IDLE, and select Run>Run Module from the menu bar. You should see an image from the camera appear on screen. The press a key to see a transformed image.</p>
<p> Once you have that working try the following:</p>
<ul>
<li>Reorienting the image if it is upside down: find the function cv2.flip(image,-1). The number in the brackets controls what sort of flip is done. Try changing it to 0 or 1, to get a correct orientation for your image, then try other numbers to see the effect.</li>
<li>Obtaining images of different sizes: change the values of variables w and h in the lines "w=480" and "h=320".</li>
<li>Adjust the blur, and try other <a href="http://docs.opencv.org/modules/imgproc/doc/filtering.html">image filtering</a> options.</li>
</ul>


## Task 2 ....


## Task 3 ....


## Task 4 ....


## Bonus Task
