#cv.VideoCapture(args.camera)
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

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))


    cv.imshow("frame",frame)
    cv.imshow("window_detection_name", frame_threshold)
    

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv.destroyAllWindows()
