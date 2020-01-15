#!/usr/bin/env python

from std_msgs.msg import Float64
import rospy
from mavros_msgs.msg import OverrideRCIn()

def kasih_print(state):
    x = state.data
    print(x)

    

if __name__ == '__main__':
    rospy.init_node('print_garis_tengah', anonymous=True)

    override_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)

    garis_subscriber = rospy.Subscriber("state1", Float64, kasih_print)

    rospy.spin()