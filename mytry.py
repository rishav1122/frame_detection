import cv2
from PIL import Image
img = cv2.imread('finalred.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
rows,cols,_ = img.shape
minx=1000
miny=1000
maxx=0
maxy=0
for i in range(rows):
      for j in range(cols):
         k = img[i,j,:]
         #print(k)
         if 240<k[2]<=255 and 240<k[1]<=255 and 10<=k[0]<=30:
            #print(k)
            if minx>i:
               minx=i
            if miny>j:
               miny=j
            if maxx<i:
               maxx=i
            if maxy<j:
               maxy=j



print(minx,miny,maxx, maxy)
print((minx+maxx)/2,(miny+maxy)/2)
cv2.rectangle(img,(miny,minx),(maxy, maxx),(0,255,0),3)
cv2.circle(img, (int((miny+maxy)/2),int((minx+maxx)/2)), 2, (255,0,0), 2)
cv2.imshow('frame',img)
cv2.waitKey(0)
