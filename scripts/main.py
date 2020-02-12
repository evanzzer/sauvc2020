#!/usr/bin/python

import os
import numpy as np
import cv2
from skimage import exposure
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image

def nothing(angka):
    pass

def RecoverCLAHE(sceneRadiance):
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4, 4))
    for i in range(3):

        # sceneRadiance[:, :, i] =  cv2.equalizeHist(sceneRadiance[:, :, i])
        sceneRadiance[:, :, i] = clahe.apply((sceneRadiance[:, :, i]))


    return sceneRadiance

rospy.init_node("MAINA")
image_publisher = rospy.Publisher("/auv/image", Image, queue_size=8)

np.seterr(over='ignore')
# cv2.startWindowThread()
# cv2.namedWindow("Trackbar")
# cv2.namedWindow("apa")
# cv2.namedWindow("op")
# cv2.namedWindow("clahe")
# cv2.createTrackbar("x", "Trackbar" , 0, 1024, nothing)
# cv2.createTrackbar("y", "Trackbar" , 0, 768, nothing)
TH = 40
vid = cv2.VideoCapture(0)
bridge = CvBridge()

while not rospy.is_shutdown():
    x = cv2.getTrackbarPos("x", "Trackbar")
    y = cv2.getTrackbarPos("y", "Trackbar")
    # img = cv2.imread('gambar.png')
    success, img = vid.read()
    if img is None:
        break
    new_img = img.copy()
    new_img = RecoverCLAHE(new_img)

    imgmsg = bridge.cv2_to_imgmsg(new_img, "bgr8")
    image_publisher.publish(imgmsg)

