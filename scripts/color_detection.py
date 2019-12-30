#!/usr/bin/env python

#ini gatau buat apaan
import cv2
import numpy as np
import time #ini buat print fps
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import Float64
# from SAUVC-2020.msg import lokasi

fps = ' '

def nothing(*arg):
    pass

if __name__ == '__main__':
    rospy.init_node('color_detection', anonymous=True)

    loc_publisher = rospy.Publisher("state/misi1", Float64, queue_size=8)

    # loc_publisher = rospy.Publisher('/auv/xloc', lokasi, queue_size=8)
    image_subscriber = rospy.Subscriber('/auv/image', Image, nothing)

    # state_publisher = rospy.Publisher("state", Float64, 8)

    cv2.namedWindow('Merah')
    cv2.namedWindow('Biru')

    cv2.createTrackbar('lowHue', 'Merah', 0, 255, nothing)
    cv2.createTrackbar('lowSat', 'Merah', 0, 255, nothing)
    cv2.createTrackbar('lowVal', 'Merah', 0, 255, nothing)
    cv2.createTrackbar('highHue', 'Merah', 255, 255, nothing)
    cv2.createTrackbar('highSat', 'Merah', 255, 255, nothing)
    cv2.createTrackbar('highVal', 'Merah', 255, 255, nothing)

    cv2.createTrackbar('lowHue', 'Biru', 0, 255, nothing)
    cv2.createTrackbar('lowSat', 'Biru', 0, 255, nothing)
    cv2.createTrackbar('lowVal', 'Biru', 0, 255, nothing)
    cv2.createTrackbar('highHue', 'Biru', 255, 255, nothing)
    cv2.createTrackbar('highSat', 'Biru', 255, 255, nothing)
    cv2.createTrackbar('highVal', 'Biru', 255, 255, nothing)

    # vidCapture = cv2.VideoCapture(0)
    # vidCapture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    # vidCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while not rospy.is_shutdown():
        gambarmsgs = rospy.wait_for_message('/auv/image', Image)
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(gambarmsgs)
        
        timeCheck = time.time() #FPS
        lowHue_merah = cv2.getTrackbarPos('lowHue', 'Merah')
        lowSat_merah = cv2.getTrackbarPos('lowSat', 'Merah')
        lowVal_merah = cv2.getTrackbarPos('lowVal', 'Merah')
        highHue_merah = cv2.getTrackbarPos('highHue', 'Merah')
        highSat_merah = cv2.getTrackbarPos('highSat', 'Merah')
        highVal_merah = cv2.getTrackbarPos('highVal', 'Merah')

        lowHue_biru = cv2.getTrackbarPos('lowHue', 'Biru')
        lowSat_biru = cv2.getTrackbarPos('lowSat', 'Biru')
        lowVal_biru = cv2.getTrackbarPos('lowVal', 'Biru')
        highHue_biru = cv2.getTrackbarPos('highHue', 'Biru')
        highSat_biru = cv2.getTrackbarPos('highSat', 'Biru')
        highVal_biru = cv2.getTrackbarPos('highVal', 'Biru')


        # _, frame = vidCapture.read()
        # cv2.imshow('original', frame)

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        colorLow_merah = np.array([lowHue_merah, lowSat_merah, lowVal_merah])
        colorHigh_merah = np.array([highHue_merah, highSat_merah, highVal_merah])

        colorLow_biru = np.array([lowHue_biru, lowSat_biru, lowVal_biru])
        colorHigh_biru = np.array([highHue_biru, highSat_biru, highVal_biru])

        mask_merah = cv2.inRange(frameHSV, colorLow_merah, colorHigh_merah)
        mask_biru = cv2.inRange(frameHSV, colorLow_biru, colorHigh_biru)

        frameblurmerah = cv2.GaussianBlur(mask_merah,(9,9), 0)
        frameblurbiru = cv2.GaussianBlur(mask_biru,(9,9), 0)

        cv2.imshow('Merah', mask_merah)
        cv2.imshow('Biru', mask_biru)

        # kontoru
        contours, _ = cv2.findContours(mask_merah, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        contourss, _ = cv2.findContours(mask_biru, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        # im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        contour_sizess = [(cv2.contourArea(contour), contour) for contour in contourss]
        success = True
        if len(contour_sizes) == 0 or len(contour_sizess) == 0: success = False
        
        # second_biggest = max(contour_sizes, key=lambda p: p[0])[1]
        if success:
            biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
            biggestt_contourr = max(contour_sizess, key=lambda x: x[0])[1]
            # bound box buat warna merah
            x,y,w,h = cv2.boundingRect(biggest_contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            lebar = int(w/2)
            tinggi = int(h/2)
            # cv2.line(frame, (x+lebar, 0), (x+lebar, 640), (255, 0, 0), 1)

            # bound box buat warna biru
            p,q,r,s = cv2.boundingRect(biggestt_contourr)
            cv2.rectangle(frame, (p, q), (p+r, q+s), (255, 0, 0), 2)
            lebarr = int(r/2)
            tinggii = int(s/2)
            # cv2.line(frame, (x+lebar, 0), (x+lebar, 640), (255, 0, 0), 1)

            x1_kotak = x+lebar
            x2_kotak = p+lebarr

            if(x1_kotak>x2_kotak):
                x_garis_tengah = (x1_kotak + x2_kotak)/2
            elif(x1_kotak<=x2_kotak):
                x_garis_tengah = (x2_kotak + x1_kotak)/2

            loc_publisher.publish(x_garis_tengah)

            cv2.line(frame, (x1_kotak, y+tinggi), (x2_kotak, q+tinggii), (0,0,0), 3)
            cv2.line(frame, (x_garis_tengah, 0), (x_garis_tengah, 640), (0,0,0), 3)

            state = Float64()
            # state.data = posisinya
            # state_publisher.publish(state)

            # xlocation = lokasi()
            # xlocation.xloc = x+lebar
            # loc_publisher.publish(xlocation)

            # p,q,r,s = cv2.boundingRect(second_biggest)
            # cv2.rectangle(frame, (p, q), (p+r, q+s), (0, 0, 255), 2)

            #print fps
            cv2.putText(frame, fps, (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

        cv2.imshow('original', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        # print('fps - ', 1/(time.time() - timeCheck))
        fps = "fps " + str(1/(time.time() - timeCheck))
    cv2.destroyAllWindows()
    vidCapture.release()