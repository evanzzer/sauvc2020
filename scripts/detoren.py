#!/usr/bin/env python

import cv2
import numpy as np
import os

def nothing(angka):
    pass

cv2.namedWindow('Merah')

filename = "videonya.avi"

cv2.createTrackbar('lowHue', 'Merah', 76, 255, nothing)
cv2.createTrackbar('lowSat', 'Merah', 92, 255, nothing)
cv2.createTrackbar('lowVal', 'Merah', 148, 255, nothing)
cv2.createTrackbar('highHue', 'Merah', 106, 255, nothing)
cv2.createTrackbar('highSat', 'Merah', 123, 255, nothing)
cv2.createTrackbar('highVal', 'Merah', 178, 255, nothing)

cap = cv2.VideoCapture('/home/amvui/Videos/Video2_new.mp4')

directory = os.path.join('/home/amvui/sauvc_ws/src/sauvc2020/scripts', filename)
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter(directory, fourcc, 30, (640, 480))

while True:
        ret, frame = cap.read()
        lowHue_merah = cv2.getTrackbarPos('lowHue', 'Merah')
        lowSat_merah = cv2.getTrackbarPos('lowSat', 'Merah')
        lowVal_merah = cv2.getTrackbarPos('lowVal', 'Merah')
        highHue_merah = cv2.getTrackbarPos('highHue', 'Merah')
        highSat_merah = cv2.getTrackbarPos('highSat', 'Merah')
        highVal_merah = cv2.getTrackbarPos('highVal', 'Merah')

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        colorLow_merah = np.array([lowHue_merah, lowSat_merah, lowVal_merah])
        colorHigh_merah = np.array([highHue_merah, highSat_merah, highVal_merah])

        mask_merah = cv2.inRange(frameHSV, colorLow_merah, colorHigh_merah)

        # cv2.imshow('Merah', mask_merah)

        # kontoru
        contours, _ = cv2.findContours(mask_merah, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        success = True
        if len(contour_sizes) < 2: success = False
        
        # second_biggest = max(contour_sizes, key=lambda p: p[0])[1]
        if success:
            aa = sorted(contour_sizes, key=lambda x: x[0], reverse=True)
            # print(aa)
            biggest_contour = aa[0][1]
            biggest_contour1 = aa[1][1]


            # bound box buat warna merah
            x,y,w,h = cv2.boundingRect(biggest_contour)
            x1,y1,w1,h1 = cv2.boundingRect(biggest_contour1)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)
            # cv2.line(frame, (x+lebar, 0), (x+lebar, 640), (255, 0, 0), 1)
            out.write(frame)

            # state.data = posisinya
            # state_publisher.publish(state)

            # xlocation = lokasi()
            # xlocation.xloc = x+lebar
            # loc_publisher.publish(xlocation)

            # p,q,r,s = cv2.boundingRect(second_biggest)
            # cv2.rectangle(frame, (p, q), (p+r, q+s), (0, 0, 255), 2)

            #print fps

        cv2.imshow('original', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        # print('fps - ', 1/(time.time() - timeCheck))
cv2.destroyAllWindows()
