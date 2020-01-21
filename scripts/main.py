#!/usr/bin/env python

import os
import numpy as np
import cv2
import natsort
import xlwt
from skimage import exposure
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

image_publisher = rospy.Publisher("/auv/image", Image, queue_size=8)

np.seterr(over='ignore')
cv2.startWindowThread()
cv2.namedWindow("Trackbar")
cv2.namedWindow("apa")
cv2.namedWindow("op")
cv2.namedWindow("clahe")
cv2.createTrackbar("x", "Trackbar" , 0, 1024, nothing)
cv2.createTrackbar("y", "Trackbar" , 0, 768, nothing)
TH = 40
vid = cv2.VideoCapture(0)
bridge = CvBridge()

while not rospy.is_shutdown():
    x = cv2.getTrackbarPos("x", "Trackbar")
    y = cv2.getTrackbarPos("y", "Trackbar")
    # img = cv2.imread('gambar.png')
    success, img = vid.read()
    new_img = img.copy()
    new_img = RecoverCLAHE(new_img)
    imgmsg = bridge.cv2_to_imgmsg(new_img, "bgr8")
    image_publisher.publish(imgmsg)
    cv2.imshow('clahe', new_img)
    cv2.imshow('apa', img)
    roi = new_img[y-5:y+5, x-5:x+5]
    h = np.mean(roi[:,:, 0])
    s = np.mean(roi[:,:, 1])
    v = np.mean(roi[:,:, 2])
    # h_low = h - TH
    # h_high = h + TH
    # s_low = s - TH
    # s_high = s + TH
    # v_low = v - TH
    # v_high = v + TH
    h_low = 74
    s_low = 84
    v_low = 100
    h_high = 164
    s_high = 174
    v_high = 190
    # print("low ", end='')
    # print((h_low, s_low, v_low))
    # print("high ", end='')
    # print((h_high, s_high, v_high))
    cv2.circle(new_img, (x,y), 5, (255, 255, 255), thickness=1, lineType=8, shift=0)
    mask1 = cv2.inRange(new_img, (h_low, s_low, v_low), (h_high, s_high, v_high))
    kernel = np.ones((15, 2) ,np.uint8)
    erosion = cv2.erode(mask1,kernel,iterations = 1)
    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200:
            continue
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(new_img, (x, y), (x + w, y + h), (0, 255,0), 2)
    cv2.imshow("apa", img)
    cv2.imshow("clahe", new_img)
    cv2.imshow("op", erosion)
    cv2.waitKey(30)
