#cv.VideoCapture(args.camera)
import cv2 as cv
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = max_value*0.3
low_V = max_value*0.35
high_H = max_value_H*0.3
high_S = max_value
high_V = max_value
import numpy as np
i=0
while i!=1:
    i=i+1
    print(i)

    frame = cv.imread("framestop.jpeg")
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    ret,thresh1 = cv.threshold(frame_threshold,127,255,cv.THRESH_BINARY_INV)
    kernel = np.ones((2,2),np.uint8)
    erosion = cv.erode(thresh1,kernel,iterations = 1)
    edges = cv.Canny(erosion,50,100,apertureSize = 3,L2gradient=True)
    minLineLength = 1
    maxLineGap = 1
    lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    print(len(lines))
    for i in range(len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv.line(frame,(x1,y1),(x2,y2),(255,0,0),2)
    """lines = cv.HoughLines(edges,1,np.pi/180,200)
    print(lines)
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

    cv.line(frame,(x1,y1),(x2,y2),(0,0,255),2)"""
    _,contours,hierarchy = cv.findContours(thresh1,2,1)

    for i in range(len(contours)):
        cnt = contours[i]

        hull = cv.convexHull(cnt,returnPoints = False)
        defects = cv.convexityDefects(cnt,hull)
        try:
            for j in range(defects.shape[0]):
                s,e,f,d = defects[j,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv.line(frame,start,end,[0,255,0],2)
                cv.circle(frame,far,5,[0,0,255],-1)
                print("yes")
        except:
            continue





    cv.imshow("canny edges",frame)
    cv.imshow("window_detection_name", frame_threshold)
    cv.imshow("binary",thresh1)
    cv.imshow("erosion",erosion)
    cv.imshow("edge",edges)

    key = cv.waitKey(0)
    if key == ord('q') or key == 27:
        break
