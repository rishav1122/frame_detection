import cv2
import numpy as np

img = cv2.imread('blackfive.png')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img,0.1,2,apertureSize = 3,L2gradient=True)
minLineLength = 1
maxLineGap = 1
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
print(len(lines))
for i in range(len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)



cv2.imshow('houghlines5.jpg',img)
cv2.waitKey(0)
