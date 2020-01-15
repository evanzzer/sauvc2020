#!/usr/bin/env python

from std_msgs.msg import Int64
from mavros_msgs.msg import OverrideRCIn
import rospy

def callbacknya(state):
    if(state.data <= 320): print("kanan")
    elif(state.data > 320): print("kiri")

if __name__ == '__main__':
    rospy.init_node('motor_misi1', anonymous=True)
    image_subscriber = rospy.Subscriber('state/misi1', Int64, callbacknya)
    rospy.spin()
 