import cv2

j=0


cap = cv2.VideoCapture("/Users/rishabkhantwal/Desktop/frame_detction/five_frames.mkv")
while True:
   j=j+1
   import time
   start = time.process_time()

   ret, img = cap.read()
   if img is None:
      break
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
   img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
   print(time.process_time() - start)
   cv2.imshow('frame',img)
   print(i,"i")











   key = cv2.waitKey(30)
   if key == ord('q') or key == 27:
        break
