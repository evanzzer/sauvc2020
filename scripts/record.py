#!/usr/bin/env python

import numpy as np
import os
import cv2
import rospy
from os import path
import threading
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError


rospy.init_node('record')
base_filename = 'video'
index = 0
filename = base_filename + str(index) + '.avi'
while path.exists(os.path.join('/home/amvui/sauvc_ws/src/sauvc2020/scripts', filename)):
    index += 1
    filename = base_filename + str(index) + '.avi'
framenya = None
# filename = 'video.avi'
frames_per_second = 30.0
res = '480p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims():
    width = 640
    height = 480
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


# cap = cv2.VideoCapture(0, cv2.CAP_V4L)
# directory = os.path.join(os.path.dirname(os.path.abspath(_file_)), filename)
directory = os.path.join('/home/amvui/sauvc_ws/src/sauvc2020/scripts', filename)
print(directory)
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter(directory, fourcc, 30, (640, 480))

try:
    while not rospy.is_shutdown():
        msgnya = rospy.wait_for_message('/auv/image', Image)
        bridge = CvBridge()
        framenya = bridge.imgmsg_to_cv2(msgnya)
        frame = framenya
        # _, frame = cap.read()
        out.write(frame)
except KeyboardInterrupt:
    out.release()
