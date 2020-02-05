#!/usr/bin/env python

import ms5837
from std_msgs.msg import Float64
import rospy

sensor = ms5837.MS5837_02BA(1)

rospy.init_node("sensor")

statepub = rospy.Publisher("/kualifikasi/state", Float64, queue_size=8)

if not sensor.init():
        print("sensor gabisa")
        exit(1)

while not rospy.is_shutdown():
    if sensor.read():
        print("P: %0.1f") % (sensor.pressure())
        status = Float64()
        status.data = sensor.pressure()
        statepub.publish(status)
    else:
        print("SENSOR GAKEBACA")
