import numpy as np
import argparse
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])
#lower=[0, 181, 247]
lower=[0, 170, 240]
upper= [10, 190, 250]
#upper=[0, 181, 248]
	# create NumPy arrays from the boundaries
lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")
	# find the colors within the specified boundaries and apply
	# the mask

mask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask = mask)
	# show the images
cv2.imshow("images",output )
cv2.waitKey(0)
