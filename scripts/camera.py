#!/usr/bin/env python

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

rospy.init_node("camera")
image_publisher = rospy.Publisher("/auv/image", Image, queue_size=8)
# compressed_image_publisher = rospy.Publisher("/auv/image/compressed", CompressedImage, queue_size=8)
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
bridge = CvBridge()
try:
    while True:
        # print("apap")
        _, data = cap.read()
        imgmsg = bridge.cv2_to_imgmsg(data, "bgr8")

        image_publisher.publish(imgmsg) # publish image biasa
        # compressed_image_publisher.publish(msg) # publish image yg ke compressed
except:
    cap.release()
