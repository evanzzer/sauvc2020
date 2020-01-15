#!/usr/bin/env python

from std_msgs.msg import Int64
from mavros_msgs.msg import OverrideRCIn()
import rospy

int control_effort

def CF_callback(cf):
    rcin = OverrideRCIn()
    for i in range (0, 8): rcin.channels[i] = 1500
    rcin.channels[] = 1500 + cf.data

 