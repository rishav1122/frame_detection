import cv2
import sys
import numpy as np
import math
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__' :



    # Set up tracker.
    # Instead of MIL, you can also use

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()# failure detection X  and no retracking
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()# no retracking
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()#retracking but only when the object returns from same area where it was last seen
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create() #retrack kar raha hai but vaise tracking ghatiya hai tho retrack karne ke liye use kar sakte hai
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()# retrack ghatiya failure detection accha
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()# dono ghatiya
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Read video
    video = cv2.VideoCapture("shape-detection/fiveframes.mkv")




    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()


    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    if not ok:
        print ('Cannot read video file')
        sys.exit()
    while 1 :

    # Define an initial bounding box
	    MIN_MATCH_COUNT = 9


	    img1 = cv2.imread('single_frame.png',0)          # queryImage
	#img2 = cv2.imread('scene.jpeg',0) # trainImage
	#cap= cv2.VideoCapture('tracking.mp4',0)

	    _,img2 = video.read()
	# Initiate SIFT detector
	    sift = cv2.xfeatures2d.SIFT_create()

	# find the keypoints and descriptors with SIFT
	    kp1, des1 = sift.detectAndCompute(img1,None)
	    kp2, des2 = sift.detectAndCompute(img2,None)

	    FLANN_INDEX_KDTREE = 0
	    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	    search_params = dict(checks = 50)

	    flann = cv2.FlannBasedMatcher(index_params, search_params)

	    matches = flann.knnMatch(des1,des2,k=2)

	# store all the good matches as per Lowe's ratio test.
	    good = []
	    for m,n in matches:
	        if m.distance < 0.7*n.distance:
	            good.append(m)
	   # print good
	    if len(good)>MIN_MATCH_COUNT:
	        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
	        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
		#print  dst_pts
	        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
	        matchesMask = mask.ravel().tolist()
	        print (len(dst_pts),len(matchesMask))
	        h,w = img1.shape
	        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
	       # print pts
	        dst = cv2.perspectiveTransform(pts,M)
	        #print M
	        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
	        q=np.int32(dst)


	        #if any corner out of box
	        if q[0][0][0]<=0 or q[0][0][0]>=639 or q[2][0][0]<=0 or q[2][0][0]>=639 or q[0][0][1]<=0 or q[0][0][1]>=479 or  q[2][0][1]<=0 or q[2][0][1]>=479:
	        	continue


	        x1=q[0][0][0]
	        x2=q[2][0][0]
	        y1=q[0][0][1]
	        y2=q[2][0][1]
	        xin= min(x1,x2)
	        yin=min(y1,y2)
	        delx=abs(x1-x2)
	        dely=abs(y1-y2)

	        #if points are very near
	        if delx<=10 or dely<=10:
	        	continue



	        bbox=(xin-25,yin-25,delx+50,dely+50)
	        ok = tracker.init(frame, bbox)
	        #bbox = cv2.selectROI(frame, False)

	        break

	    else:
	        print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
	        matchesMask = None

	    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
	                       singlePointColor = None,
	                       matchesMask = matchesMask, # draw only inliers
	                       flags = 2)
	    #img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
	    #cv2.imshow('kachra',img3)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

	xupin=bbox[0]
	yupin=bbox[1]
	delupx=bbox[2]
	delupy=bbox[3]




 	frame[(yupin+ math.floor(delupy/2))-3:(yupin+math.floor(delupy/2))+3,(xupin+math.floor(delupx/2))-3:(xupin+math.floor(delupx/2))+3]=[0,0,255]
#frame[(yin+dely/2)-10:(yin+del/2)+10,(xin+delx/2)-10:(xin+delx/2)+10]=[0,0,25]
        # Display result
        cv2.imshow("Tracking", frame)
#frame[(xin+delx/2)-10:(xin+delx/2)+10,(yin+dely/2)-10:(yin+dely/2)+10]=[0,0,0]
 	#frame[(xin+delx/2)-3:(xin,(yin+dely/2)]=(0,0,255)
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
############
