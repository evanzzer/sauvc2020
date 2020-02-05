#!/usr/bin/env python

from std_msgs.msg import Float64
import rospy

pertama = None

def compass_callback(msg):
	global pertama
	yaw = msg.data
	# print(yaw)
	if(pertama==None):
		pertama = yaw
	
	status = Float64()
	status.data = pertama
	compass_pub.publish(status)

	status_state = Float64()
	status_state.data = yaw
	compass_pub_state.publish(status_state)



if __name__== "__main__":
	rospy.init_node("yaaaww")

	compass_pub = rospy.Publisher("/compass/setpoint", Float64, queue_size=10)
	compass_pub_state = rospy.Publisher("/compass/state", Float64, queue_size=10)
	compass_sub = rospy.Subscriber("/mavros/global_position/compass_hdg", Float64, compass_callback, queue_size=10)


	rospy.spin()
