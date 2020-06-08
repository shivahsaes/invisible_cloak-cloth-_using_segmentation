print("Steps:\n 1. Capture and store the BACKGROUND Image. \n 2.Detect the colored cloth( here the color is red) using color detection and segmentation.\n 3.Segment out the colored cloth by generating a mask.\n 4.Generate the final augumented output to create masked effect.")

#importing required libraries
import numpy as np
import cv2
import time

#creating a video source
cap=cv2.VideoCapture('Testvideo1.mp4')

#giving time for camera to capture the background
time.sleep(2)

#creating a BG image that is to display
BG=0
#here im giving 30 iterations to capture   BG
for i in range(30):
    ret, bg = cap.read()

while(cap.isOpened()):
    ret, img = cap.read()

    if not ret:
        break
    #coverting BGR image into HSV image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #HSV VALUES FOR RED COLOR

    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])

    #seperation the cloth
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])

    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2


    #here, in above if any shades b/w 0 to 10 and 170 to 180 then its segemnted

    #noise removal
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations=1)

    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(bg, bg, mask = mask1)
    res2 = cv2.bitwise_and(img, img, mask = mask2)

    #output video

    op = cv2.addWeighted(res1,1,res2,1,0)
    op=cv2.resize(op,(500,350))

    cv2.imshow('output',op)
    
    k = cv2.waitKey(10)
    if k==27:
        break


    




