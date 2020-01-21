#!/usr/bin/env python

import ms5837
import time
import rospy
from std_msgs.msg import Float64, Int16
from mavros_msgs.msg import OverrideRCIn

sensor = ms5837.MS5837_02BA(1) # Default I2C bus is 1 (Raspberry Pi 3)
motor_pub = None
kecepatan = 1600

def control_effort_callback(msg):
    control_effort = msg.data
    rcin = OverrideRCIn()
    rcin.channels[5] = 1500 + control_effort
    rcin.channels[6] = 1500 + control_effort
    motor_pub.publish(rcin)


def release():
    rcin = OverrideRCIn()
    for i in range (0, 8): rcin.channels[i] = 1500
    rospy.loginfo("release")
    motor_pub.publish(rcin)	


def start():
    rcin = OverrideRCIn()
    for i in range (0, 8): rcin.channels[i] = 1500
    rospy.loginfo("Start")
    for i in range (1, 5): rcin.channels[i] = 1600
    motor_pub.publish(rcin)	

def naikturun():
    global tread_active
    while not rospy.is_shutdown():
        if not tread_active:
            if sensor.read():
                state = Float64()
                state.data = sensor.pressure()
                print(state)
                state_publisher(state)
                sleep(0.2)


def killcallback(msg):
	oke = msg.data
	if(oke==0):
		# rospy.loginfo("islive")
		global tread_active
		tread_active = False
		global prev_callback_state
		
		if oke == prev_callback_state:
			return
		prev_callback_state = 0
		start()
	else:
		# rospy.loginfo("isDead")
		global tread_active
		tread_active = True
		global prev_callback_state
		prev_callback_state = 1

if __name__ == '__main__':
    rospy.init_node('kualifikasi_PID', anonymous=True)

    state_publisher = rospy.Publisher("kualifikasi/state", Float64, queue_size=8)
    motor_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=10)
    controleffort_subscriber = rospy.Subscriber("kualifikasi/control_effort", Float64, control_effort_callback, queue_size=10)
    killswitch_sub = rospy.Subscriber("kill_switch", Int16, killcallback, queue_size=10)

    # inisialisasi
    if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)
    release()
    sleep(2)
    start()
    sleep(2)
    tread = threading.Thread(target=naikturun)
    tread.start()
    rospy.spin()
    