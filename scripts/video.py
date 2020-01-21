#!/usr/bin/env python

import rospy
from mavros_msgs.msg import OverrideRCIn
from time import sleep

def init():
    rc = OverrideRCIn()
    for i in range(0,8):
        rc.channels[i] = 1500
    override_publisher.publish(rc)

def turun():
    rc = OverrideRCIn()
    for i in range(0, 8): rc.channels[i] = 1500
    for i in range(0, 2):
        rc.channels[i] = 1400
    override_publisher.publish(rc)

def maju():
    rc = OverrideRCIn()
    for i in range(0, 8): rc.channels[i] = 1500
    for i in range(2, 6):
        rc.channels[i] = 1600
    override_publisher.publish(rc)

if __name__ == '__main__':
    rospy.init_node('video')
    override_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=8)
    while not rospy.is_shutdown():
        print("sini")
        init()
        sleep(5)
        turun()
        sleep(2)
        maju()
        sleep(8)
