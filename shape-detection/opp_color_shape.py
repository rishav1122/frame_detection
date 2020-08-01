import cv2 as cv
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = max_value*0.3
low_V = max_value*0.35
high_H = max_value_H*0.3
high_S = max_value
high_V = max_value
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2 as cv
import numpy as np
i=0
while i!=1:
    i=i+1
    print(i)

    frame = cv.imread("nearst.png")
    if frame is None:
        print("image not found")
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    ret,thresh1 = cv.threshold(frame_threshold,127,255,cv.THRESH_BINARY_INV)




# construct the argument parse and parse the arguments


image=thresh1
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it


# find contours in the thresholded image and initialize the
# shape detector
cnts = cv.findContours(thresh1.copy(), cv.RETR_EXTERNAL,
	cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

# loop over the contours
for c in cnts:
	print("kkk")
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv.moments(c)
	#print(M)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)


	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv.drawContours(image, [c], -1, (0, 255, 0), 2)

	cv.putText(image, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)
	print(cX,cY)

	# show the output image
	cv.imshow("Image", image)
	cv.waitKey(0)
