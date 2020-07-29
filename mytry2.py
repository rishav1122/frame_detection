import cv2

from PIL import Image
im = Image.open('red.jpg')
pixelMap = im.load()
image=cv2.imread('red.jpg')
img = Image.new( im.mode, im.size)
pixelsNew = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if j<20 or j>75 or i>195 or i<105:
            image[j,i]=(255,255,255)
        else:
            pixelsNew[i,j] = pixelMap[i,j]
image[25:70,110:190]=(255,255,255)
cv2.imshow('fg',image)
cv2.imwrite('finalred.png',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
