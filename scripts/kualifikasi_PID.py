#!/usr/bin/env python

import ms5837
import time
import rospy
from std_msgs.msg import Float64, Int16
from mavros_msgs.msg import OverrideRCIn
import threading
from datetime import datetime

prev_callback_state = -1
sensor = ms5837.MS5837_02BA(1)
motor_pub = None
state_publisher = None
control_effort = 0
kecepatan = 1600

def control_effort_callback(msg):
    control_effort = msg.data
    rcin = OverrideRCIn()
    rcin.channels[1] = 1500 + control_effort
    rcin.channels[4] = 1500 + control_effort
    rcin.channels[0] = kecepatan
    rcin.channels[2] = kecepatan
    rcin.channels[3] = kecepatan
    rcin.channels[5] = kecepatan
    motor_pub.publish(rcin)
    time.sleep(0.5)

def release():
    rcin = OverrideRCIn()
    for i in range (0, 8): rcin.channels[i] = 1500
    rospy.loginfo("release")
    motor_pub.publish(rcin)	

def start():
    rcin = OverrideRCIn()
    for i in range (0, 8): rcin.channels[i] = 1500
    rospy.loginfo("Start")
    rcin.channels[0] = kecepatan
    rcin.channels[2] = kecepatan
    rcin.channels[3] = kecepatan
    rcin.channels[5] = kecepatan
    motor_pub.publish(rcin)
    # rospy.loginfo("MAJU")

def naikturun():
    global tread_active
    # rospy.loginfo("sini")
    prev_state = -1
    refreshed = False
    while not rospy.is_shutdown():
        if not tread_active:
            prev_state = -1
            refreshed = True
            continue
	# rospy.loginfo("paan")
	if(refreshed):
		start()
		refreshed= False
        if sensor.read():
            waktusekarang = time.time()
            print(str(int(waktusekarang)))
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            file1 = open("/home/amvui/sauvc_ws/src/sauvc2020/scripts/data_press.txt", "a")
            file1.write(current_time + "DEPTH:  " + str(sensor.pressure()) + "\n")
            file1.close()
                
            status = Float64()
            status.msg = int(sensor.pressure())
            state_publisher.publish(status)
                
def killcallback(msg):
	oke = msg.data
	if(oke==0):
		# rospy.loginfo("MATI")
		global tread_active
		tread_active = False
		global prev_callback_state
		if oke == prev_callback_state:
			return
		prev_callback_state = 0
		release()

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
    time.sleep(5)
    
    # inisialisasi
    if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)
    release()
    time.sleep(2)
    # start()
    # time.sleep(2)
    tread = threading.Thread(target=naikturun)
    tread.start()
    rospy.spin()
