#!/usr/bin/env python

import ms5837
import time
import rospy
import mavros_msgs.msg

sensor = ms5837.MS5837_02BA(1) # Default I2C bus is 1 (Raspberry Pi 3)

if not sensor.init():
        print("sensor gabisa")
        exit(1)

while not rospy.is_shutdown():
        if sensor.read():
                if(sensor.pressure()<50):
                        print("turun")
                else:
                        print("MAJU")
        else:
                print("FAILED")
                exit(1)