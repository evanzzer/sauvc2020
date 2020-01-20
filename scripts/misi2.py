#!/usr/bin/env python

import numpy as np
import cv2
import random
import rospy
from mavros_msgs.msg import RCIn
from std_msgs.msg import Float64
from sensor_msgs.msg import Image, CompressedImage
import time
from mavros_msgs.msg import OverrideRCIn
from cv_bridge import CvBridge, CvBridgeError

seconds = 0
local_time = time.ctime(seconds)
mtr_pub = None #publisher motor nya
lineThickness = 1 #ketebalanGaris
font = cv2.FONT_HERSHEY_COMPLEX #Jenis fontnya
data = None
# state_publisher = rospy.Publisher("state", Float64, queue_size=10) # define pengirim/publisher dari state , tipe data float64 , queue size 10 
rospy.init_node('DetekBiruuu1', anonymous=True) #inisiasi node DetekBiru3 image_subscriber = rospy.Subscriber('/auv/image', Image, nothing) #define image subsciber/penerima
mtr_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=10) #define publisher/pengirim ovveride rcin
waktusekarang = time.time()    
fps = ' '

def nothing(img):
    pass

##detek warna biru 

# cv2.startWindowThread()
cv2.namedWindow("Trackbars")
cv2.namedWindow("Frame")
cv2.namedWindow("blue_mask")
cv2.createTrackbar("BLUE L-H", "Trackbars", 44, 255, nothing)
cv2.createTrackbar("BLUE L-S", "Trackbars", 196, 255, nothing)
cv2.createTrackbar("BLUE L-V", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("BLUE U-H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("BLUE U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("BLUE U-V", "Trackbars", 255, 255, nothing)

image_subscriber = rospy.Subscriber('/auv/image', Image, nothing)
# do stuff
#while True : #ketika kondisinya benar

while not rospy.is_shutdown():
    
    data = rospy.wait_for_message("/auv/image" , Image)
    refreshed = False
    # do stuff
           
    bridge = CvBridge()
    ori = bridge.imgmsg_to_cv2(data)
    frame = ori.copy()
    #_,img=cap.read() #baca image capture
    #gambarmsgs = rospy.wait_for_message('/auv/image', Image)
    #bridge = CvBridge()
    
    #frame = img.copy() # image dicopy 
    #frame = img.copy(gambarmsgs) # image dicopy 
 
#jadiin HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #ubah jadi HSV
    hsv = cv2.GaussianBlur(hsv, (5, 5), 1) #diblur 

    # BIRU
    l_h = cv2.getTrackbarPos("BLUE L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("BLUE L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("BLUE L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("BLUE U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("BLUE U-S", "Trackbars")    
    u_v = cv2.getTrackbarPos("BLUE U-V", "Trackbars")

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    
    success = True
    
    if len(contour_sizes) == 0 : success = False #jikaru contur biru nya ga kedetek
    
    if success == True:
        # global waktusekarang
        waktusekarang = time.time()
    if success == False:
        waktusaatini = time.time()
        waktuanu = waktusaatini - waktusekarang
        print(waktuanu)
        if waktuanu > 5 :
              
            rcin = OverrideRCIn() #diovverride 
            for i in range (0, 8): rcin.channels[i] = 1500 
            rcin.channels[6] = 1700
            rospy.loginfo("buka gripper")
            mtr_pub.publish(rcin)  
              

    max_area = 0
    max_contour = None
    max_x = 0
    state = Float64()
    # state.data = posisinya
    # state_publisher.publish(state)
    if success :
        
        #cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)              
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        # bound box buat warna biru 
        x,y,w,h = cv2.boundingRect(biggest_contour)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        lebar = int(w/2)
        tinggi = int(h/2)
            
        cv2.line(frame, (x+lebar, 0), (x+lebar, 640), (255, 0, 0), 1)  

        if x < 320 :
            rcin = OverrideRCIn()
            for i in range (0, 8): rcin.channels[i] = 1500
            rcin.channels[1] = 1600
            rcin.channels[2] = 1400
            rcin.channels[3] = 1400
            rcin.channels[4] = 1600
            rospy.loginfo("Roll Kiri")
            mtr_pub.publish(rcin)
        else:
            rcin = OverrideRCIn()
            for i in range (0, 8): rcin.channels[i] = 1500
            rcin.channels[1] = 1400
            rcin.channels[2] = 1600
            rcin.channels[3] = 1600
            rcin.channels[4] = 1400
            rospy.loginfo("Roll Kanan ")
            mtr_pub.publish(rcin)
            
        if y < 240:
            rcin = OverrideRCIn()
            for i in range (0, 8): rcin.channels[i] = 1500
            rcin.channels[5] = 1550
            rcin.channels[6] = 1550
            rospy.loginfo("turun")
            mtr_pub.publish(rcin)   
        else:   
            rcin = OverrideRCIn()
            for i in range (0, 8): rcin.channels[i] = 1500
            rcin.channels[5] = 1450
            rcin.channels[6] = 1450
            rospy.loginfo("naik")
            mtr_pub.publish(rcin)    
   
    cv2.putText(frame, fps, (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)  
    cv2.imshow("Frame", frame)
    cv2.imshow("blue_mask", blue_mask)
    cv2.waitKey(30)
    
 
