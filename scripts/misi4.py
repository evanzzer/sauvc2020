#!/usr/bin/env python

from __future__ import division #ini gatau buat apaan
import cv2
import numpy as np
import time #ini buat print fps
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import Float64, Int16
from mavros_msgs.msg import OverrideRCIn
import threading

kecepatan = 1550
angka = 20
motor_pub = None

# from SAUVC-2020.msg import lokasi

def nothing(*arg):
    pass

def killcallback(msg):
        # print(msg.data)
	oke = msg.data
	if(oke==0):
		# rospy.loginfo("MATI")
		global tread_active
		tread_active = False
		global prev_callback_state
		if oke == prev_callback_state:
			return
		prev_callback_state = 0
		release()

	else:
		# rospy.loginfo("isDead")
		global tread_active
		tread_active = True
		global prev_callback_state
		prev_callback_state = 1

def release():
    rcin = OverrideRCIn()
    for i in range (0, 8): rcin.channels[i] = 1500
    rospy.loginfo("release")
    motor_pub.publish(rcin)

def naikturun():
    global tread_active
    # rospy.loginfo("sini")
    prev_state = -1
    refreshed = False
    tread_active = True
    # print("aaaa")
    while not rospy.is_shutdown():
        # print("t")
        if not tread_active:
            # print("maticuy")
            prev_state = -1
            refreshed = True
            continue
	# rospy.loginfo("paan")
	if(refreshed):
	    release()
            refreshed= False
            continue
        if tread_active:
            gambarmsgs = rospy.wait_for_message('/auv/image', Image)
            bridge = CvBridge()
            frame = bridge.imgmsg_to_cv2(gambarmsgs)

            # frame = cv2.imread('/home/nathan/Pictures/1.png')

            # timeCheck = time.time() #FPS
            # lowHue_kuning = cv2.getTrackbarPos('lowHue', 'kuning')
            # lowSat_kuning = cv2.getTrackbarPos('lowSat', 'kuning')
            # lowVal_kuning = cv2.getTrackbarPos('lowVal', 'kuning')
            # highHue_kuning = cv2.getTrackbarPos('highHue', 'kuning')
            # highSat_kuning = cv2.getTrackbarPos('highSat', 'kuning')
            # highVal_kuning = cv2.getTrackbarPos('highVal', 'kuning')

            lowHue_kuning = 76
            lowSat_kuning = 65
            lowVal_kuning = 22
            highHue_kuning = 121
            highSat_kuning = 158
            highVal_kuning = 191

            frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            colorLow_kuning = np.array([lowHue_kuning, lowSat_kuning, lowVal_kuning])

            colorHigh_kuning = np.array([highHue_kuning, highSat_kuning, highVal_kuning])

            kuning_mask = cv2.inRange(frameHSV, colorLow_kuning, colorHigh_kuning)

            frameblurkuning = cv2.GaussianBlur(kuning_mask,(9,9), 0)

            cv2.imshow('kuning', kuning_mask)

            # kontoru
            contours, _ = cv2.findContours(kuning_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

            # im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
            success = True
            if len(contour_sizes) == 0: success = False

            # second_biggest = max(contour_sizes, key=lambda p: p[0])[1]
            if success:
                biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
            #titiktengah
                area = cv2.contourArea(biggest_contour)
                approx = cv2.approxPolyDP(biggest_contour, 0.02*cv2.arcLength(biggest_contour, True), True)
                M = cv2.moments(biggest_contour)
                if M["m00"] == 0:
                    continue
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
                cv2.drawContours(frame,[approx] , 0, (0, 0, 0), 5)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                cv2.line(frame, (x, 0), (x, 480), (0,0,0), 3)

                # state = Float64()

                if x == 320:
                    rcin = OverrideRCIn()
                    rcin.channels[0] = kecepatan
                    rcin.channels[1] = 1500
                    rcin.channels[2] = kecepatan
                    rcin.channels[3] = kecepatan
                    rcin.channels[4] = 1500
                    rcin.channels[5] = kecepatan
                    rcin.channels[6] = 1500
                    rcin.channels[7] = 1500
                    rospy.loginfo("Maju")
                    print(x)
                    motor_pub.publish(rcin)

                if x > 320:
                    rcin = OverrideRCIn()
                    rcin.channels[0] = kecepatan - angka
                    rcin.channels[1] = 1500
                    rcin.channels[2] = kecepatan - angka
                    rcin.channels[3] = kecepatan + angka
                    rcin.channels[4] = 1500
                    rcin.channels[5] = kecepatan + angka
                    rcin.channels[6] = 1500
                    rcin.channels[7] = 1500
                    rospy.loginfo("Belok Kanan")
                    print(x)
                    motor_pub.publish(rcin)

                if x < 320:
                    rcin = OverrideRCIn()
                    rcin.channels[0] = kecepatan + angka
                    rcin.channels[1] = 1500
                    rcin.channels[2] = kecepatan + angka
                    rcin.channels[3] = kecepatan - angka
                    rcin.channels[4] = 1500
                    rcin.channels[5] = kecepatan - angka
                    rcin.channels[6] = 1500
                    rcin.channels[7] = 1500
                    rospy.loginfo("Belok Kiri")
                    print(x)
                    motor_pub.publish(rcin)
                
            else: # KALO GA KETEMU APA-APA DIA MUTER-MUTER
                rcin = OverrideRCIn()
                rcin.channels[0] = 1500 + 20
                rcin.channels[1] = 1500
                rcin.channels[2] = 1500 + 20
                rcin.channels[3] = 1500 - 20
                rcin.channels[4] = 1500
                rcin.channels[5] = 1500 - 20
                rcin.channels[6] = 1500
                rcin.channels[7] = 1500
                rospy.loginfo("Belok Kiri")
                print(x)
                motor_pub.publish(rcin)

                # cv2.putText(frame, "mission4", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
        #     cv2.imshow('original', frame)
        #     k = cv2.waitKey(5) & 0xFF
        #     if k == 27:
        #         break
        # cv2.destroyAllWindows()
        # vidCapture.release()
        time.sleep(0.2)

#KODINGAN DIBUAT DENGAN KONDISI BELUM MENGGUNAKAN SENSOR KEDALAMAN
#DENGAN KONDISI AUV SUDAH SETARA DENGAN TIANG KUNING

if __name__ == '__main__':
    rospy.init_node('MissionFour', anonymous=True)
    motor_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=10)
    # loc_publisher = rospy.Publisher('/auv/xloc', lokasi, queue_size=8)
    image_subscriber = rospy.Subscriber('/auv/image', Image, nothing)
    killswitch_sub = rospy.Subscriber("kill_switch", Int16, killcallback, queue_size=10)

    cv2.namedWindow('kuning')

    release()
    time.sleep(2)
    tread = threading.Thread(target=naikturun)
    tread.start()
    rospy.spin()

    # cv2.createTrackbar('lowHue', 'kuning', 0, 255, nothing)
    # cv2.createTrackbar('lowSat', 'kuning', 0, 255, nothing)
    # cv2.createTrackbar('lowVal', 'kuning', 0, 255, nothing)
    # cv2.createTrackbar('highHue', 'kuning', 255, 255, nothing)
    # cv2.createTrackbar('highSat', 'kuning', 255, 255, nothing)
    # cv2.createTrackbar('highVal', 'kuning', 255, 255, nothing)


