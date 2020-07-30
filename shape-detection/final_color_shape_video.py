
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import numpy as np
import cv2 as cv
max_value = 255
max_value_H = 360//2
low_H = max_value_H*0.1
low_S = max_value*0.3
low_V = max_value*0.35
high_H = max_value_H*0.25
high_S = max_value
high_V = max_value
cap=cv.VideoCapture("five_frames.mkv")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)
result = cv.VideoWriter('filename.avi',
                         cv.VideoWriter_fourcc(*'MJPG'),
                         200000000.0, size)
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))


    # the shapes can be approximated better
    """
    resized = imutils.resize(frame_threshold, width=300)
    ratio = frame.shape[0] / float(resized.shape[0])


    #gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(resized, (5, 5), 0)
    thresh = cv.threshold(blurred, 60, 255, cv.THRESH_BINARY)[1]

    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
    	cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    # loop over the contours
    for c in cnts:
        M = cv.moments(c)
        if  M["m00"]==0:
            break
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv.drawContours(frame_threshold, [c], -1, (0, 255, 0), 2)
        cv.putText(frame_threshold, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
        print(cX,cY)
        cv.imshow("Image", frame_threshold)
        key=cv.waitKey(0)
        if key == ord('q') or key == 27:
            continue"""


    edges = cv.Canny(frame_threshold,0.1,2,apertureSize = 3,L2gradient=True)
    minLineLength = 10
    maxLineGap = 10
    lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv.line(frame_threshold,(x1,y1),(x2,y2),(0,255,0),2)


    cv.imshow('houghlines5.jpg',frame_threshold)
    cv.waitKey(0)






    cv.imshow("frame",frame)
    cv.imshow("window_detection_name", frame_threshold)
    result.write(frame_threshold)

    key = cv.waitKey(0)
    if key == ord('q') or key == 27:
        break
cap.release()
result.release()
cv.destroyAllWindows()
