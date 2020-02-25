#!/usr/bin/env python

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

scale_percent = 50

def RecoverCLAHE(sceneRadiance):
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4, 4))
    for i in range(3):

        # sceneRadiance[:, :, i] =  cv2.equalizeHist(sceneRadiance[:, :, i])
        sceneRadiance[:, :, i] = clahe.apply((sceneRadiance[:, :, i]))


    return sceneRadiance



rospy.init_node("camera")
image_publisher = rospy.Publisher("/auv/image", Image, queue_size=8)
# compressed_image_publisher = rospy.Publisher("/auv/image/compressed", CompressedImage, queue_size=8)
cap = cv2.VideoCapture(0)
bridge = CvBridge()
try:
    while not rospy.is_shutdown():
        # print("apap")
        _, data = cap.read()
        data = RecoverCLAHE(data)

	width = int(data.shape[1] * scale_percent / 100)
	height = int(data.shape[0] * scale_percent / 100)

	dsize = (640, 480)

	output = cv2.resize(data, dsize)
        imgmsg = bridge.cv2_to_imgmsg(data, "bgr8")
        image_publisher.publish(imgmsg) # publish image biasa
	# cv2.imshow("test", output)
	cv2.waitKey(30)
except:
    cap.release()
