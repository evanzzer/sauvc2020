#!/usr/bin/env python

import ms5837
import time
import rospy
from mavros_msgs.msg import OverrideRCIn

sensor = ms5837.MS5837_02BA() # Default I2C bus is 1 (Raspberry Pi 3)

override_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)

if not sensor.init():
        print("sensor gabisa")
        exit(1)

while not rospy.is_shutdown():
        if sensor.read():
                if(sensor.pressure()<50):
                        # rcin = OverrideRCIn()
                        # rcin.channels[0] = 1600
                        # rcin.channels[1] = 1600
                        # override_publisher.publish(rcin)
                        print("turun")
                else:
                        # rcin = OverrideRCIn()
                        # rcin.channels[0] = 0
                        # rcin.channels[1] = 0
                        # rcin.channels[2] = 1600
                        # rcin.channels[3] = 1600
                        # rcin.channels[4] = 1600
                        # rcin.channels[5] = 1600
                        # override_publisher.publish(rcin)
                        print("MAJU")
        else:
                print("FAILED")
                exit(1)