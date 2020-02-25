#!/usr/bin/env python

import time
import rospy
from std_msgs.msg import Float64, Int64, Int16
from mavros_msgs.msg import OverrideRCIn
import threading
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from sensor_msgs.msg import Image, CompressedImage
from sauvc.msg import Kontrol
import math

prev_callback_state = -1
motor_pub = None
loc_pub = None
kontrol_pub = None
kecepatan = 1600
toleransi = 20
control_effort = None
status = None

def control_effort_callback(msg):
    control_effort = msg.data

def kontrolcallback(msg):
    status = msg.misiSatu_mulai

def nothing(*arg):
    pass

def release():
    rcin = OverrideRCIn()
    for i in range (0, 8): rcin.channels[i] = 1500
    rospy.loginfo("release")
    motor_pub.publish(rcin)	

def naikturun():
    # print("masuk sini")
    global tread_active
    prev_state = -1
    refreshed = False
    tread_active = True
    while not rospy.is_shutdown():
        # print("masuk")
        if not tread_active:
            prev_state = -1
            refreshed = True
            continue
	# rospy.loginfo("paan")
	    if(refreshed):
		    release()
		    refreshed= False
        gambarmsgs = rospy.wait_for_message('/auv/image', Image)
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(gambarmsgs)

        lowHue_merah = -10
        lowSat_merah = 90
        lowVal_merah = 90
        highHue_merah = 10
        highSat_merah = 110
        highVal_merah = 110

        lowHue_biru = 230
        lowSat_biru = 90
        lowVal_biru = 90
        highHue_biru = 250
        highSat_biru = 110
        highVal_biru = 110

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        colorLow_merah = np.array([lowHue_merah, lowSat_merah, lowVal_merah])
        colorHigh_merah = np.array([highHue_merah, highSat_merah, highVal_merah])

        colorLow_biru = np.array([lowHue_biru, lowSat_biru, lowVal_biru])
        colorHigh_biru = np.array([highHue_biru, highSat_biru, highVal_biru])

        mask_merah = cv2.inRange(frameHSV, colorLow_merah, colorHigh_merah)
        mask_biru = cv2.inRange(frameHSV, colorLow_biru, colorHigh_biru)

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

            # bound box buat warna biru
            p,q,r,s = cv2.boundingRect(biggestt_contourr)
            cv2.rectangle(frame, (p, q), (p+r, q+s), (255, 0, 0), 2)
            lebarr = int(r/2)
            tinggii = int(s/2)

            x1_kotak = x+lebar
            x2_kotak = p+lebarr

            if(x1_kotak>x2_kotak):
                x_garis_tengah = (x1_kotak + x2_kotak)/2
            elif(x1_kotak<=x2_kotak):
                x_garis_tengah = (x2_kotak + x1_kotak)/2

            # INI PUBLISH GARIS TENGAH
            state = Int64()
            state.data = x_garis_tengah
            loc_pub.publish(state)
            # print(state.data)

            #INI BUAT PRINT GARIS GARIS
            cv2.line(frame, (x1_kotak, y+tinggi), (x2_kotak, q+tinggii), (0,0,0), 3)
            cv2.line(frame, (x_garis_tengah, 0), (x_garis_tengah, 640), (0,0,0), 3)

            rcin = OverrideRCIn()
            if(abs(control_effort) == toleransi):
                # MAJU
                rcin.channels[0] = 1550
                rcin.channels[2] = 1550
                rcin.channels[3] = 1550
                rcin.channels[5] = 1550
                motor_pub.publish(rcin)

            else:
                # BELOK-BELOK
                rcin.channels[0] = 1500 - control_effort 
                rcin.channels[2] = 1500 + control_effort
                rcin.channels[3] = 1500 + control_effort
                rcin.channels[5] = 1500 - control_effort
                motor_pub.publish(rcin)
        else:
            selesai = Kontrol()
            selesai.misiSatu_selesai = True
            kontrol_pub.publish(selesai)

        # print("abc")    
        # cv2.imshow('original', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        cv2.destroyAllWindows()
        # VidCapture.release()
        
                
def killcallback(msg):
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

if __name__ == '__main__':
    rospy.init_node('misiSATU', anonymous=True)

    motor_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=10)
    loc_pub = rospy.Publisher("misi1/state", Int64, queue_size=8)
    kontrol_pub = rospy.Publisher("statusmisi_selesai", Kontrol, queue_size=10)

    controleffort_subscriber = rospy.Subscriber("misi1/control_effort", Float64, control_effort_callback, queue_size=10)
    killswitch_sub = rospy.Subscriber("kill_switch", Int16, killcallback, queue_size=10)
    kontrol_sub = rospy.Subscriber("statusmisi_mulai", Kontrol, kontrolcallback, queue_size=10)
    image_subscriber = rospy.Subscriber('/auv/image', Image, nothing)

    cv2.namedWindow('Merah')
    cv2.namedWindow('Biru')

    time.sleep(5)


    # inisialisasi
    release()
    time.sleep(2)
    tread = threading.Thread(target=naikturun)
    tread.start()
    rospy.spin()
