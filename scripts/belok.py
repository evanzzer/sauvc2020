#!/usr/bin/env python

from mavros_msgs.msg import OverrideRCIn
from std_msgs.msg import Int16, Float64

awal = None

def kanan(msg):
	state = msg.data
	rospy.loginfo(state)
	
	global awal
	if (awal == None): awal = state
	
	delta = state-awal
	if not ( 85 <= delta <= 95 ):
		rcin = OverrideRCIn()
        	for i in range (0, 8): rcin.channels[i] = 1500
        	rcin.channels[2] = 1450
        	rcin.channels[3] = 1450
        	rcin.channels[4] = 1550
        	rcin.channels[5] = 1550
		rospy.loginfo("Kiri")
        	motor_pub.publish(rcin)
	else:
	for i in range (0, 8): rcin.channels[i] = 1500 
	return

def kiri(msg):
	state = msg.data
	rospy.loginfo(state)
	
	global awal
	if (awal == None): awal = state
	
	delta = state-awal
	if not ( -85 <= delta <= -95 ):
		rcin = OverrideRCIn()
        	for i in range (0, 8): rcin.channels[i] = 1500
        	rcin.channels[2] = 1550
        	rcin.channels[3] = 1550
        	rcin.channels[4] = 1450
        	rcin.channels[5] = 1450
		rospy.loginfo("Kiri")
        	motor_pub.publish(rcin)
	else:
		for i in range (0, 8): rcin.channels[i] = 1500 
		return
	

if __name__=="__main__":

	rospy.init_node("majumundur")
	compass_sub_kanan = rospy.Subscriber("/mavros/global_position/compass_hdg",Float64, kanan, queue_size=10)
	compass_sub_kiri = rospy.Subscriber("/mavros/global_position/compass_hdg",Float64, kiri, queue_size=10)
	
	rospy.spin()


