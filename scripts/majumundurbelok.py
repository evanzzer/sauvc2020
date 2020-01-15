#!/usr/bin/env python

from mavros_msgs.msg import OverrideRCIn
from std_msgs.msg import Int16, Float64
from time import sleep
import ctypes

import time
import rospy
import threading

motor_pub = None
oke = None
tread_active = True
prev_callback_state = 1

derajat_awal = None
derajat_skrg = None



def naik():
        rcin = OverrideRCIn()
        for i in range (0, 8): rcin.channels[i] = 1500
        rcin.channels[0] = 1600
        rcin.channels[1] = 1600
	rospy.loginfo("Naik")
        motor_pub.publish(rcin)

def turun():
        rcin = OverrideRCIn()
        for i in range (0, 8): rcin.channels[i] = 1500
        rcin.channels[0] = 1400
        rcin.channels[1] = 1400
	rospy.loginfo("Turun")
        motor_pub.publish(rcin)

def maju():
        rcin = OverrideRCIn()
        for i in range (0, 8): rcin.channels[i] = 1500
        rcin.channels[2] = 1550
        rcin.channels[3] = 1550
        rcin.channels[4] = 1550
        rcin.channels[5] = 1550
	rospy.loginfo("Maju")
        motor_pub.publish(rcin)


def mundur():
	rcin = OverrideRCIn()
        for i in range (0, 8): rcin.channels[i] = 1500
        rcin.channels[2] = 1450
        rcin.channels[3] = 1450
        rcin.channels[4] = 1450
        rcin.channels[5] = 1450
	rospy.loginfo("Mundur")
        motor_pub.publish(rcin)

def belok(msg):
	global derajat_skrg
	derajat_skrg = msg.data

def kanan():
	state = derajat_skrg
	rospy.loginfo(state)
	
	global derajat_awal
	if (derajat_awal == None): derajat_awal = derajat_skrg
	
	delta = derajat_skrg-derajat_awal
	if not ( 85 <= delta <= 95 ):
		rcin = OverrideRCIn()
        	for i in range (0, 8): rcin.channels[i] = 1500
        	rcin.channels[2] = 1450
        	rcin.channels[3] = 1450
        	rcin.channels[4] = 1550
        	rcin.channels[5] = 1550
		rospy.loginfo("Kanan")
        	motor_pub.publish(rcin)
		return False
	else:
		for i in range (0, 8): rcin.channels[i] = 1500 
		return True


def roll():
	rcin = OverrideRCIn()
        for i in range (0, 8): rcin.channels[i] = 1500
        rcin.channels[0] = 1400
        rcin.channels[1] = 1600
	rospy.loginfo("Roll")
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
        motor_pub.publish(rcin)	
		
def naikturun():
	prev_state = 0
	awal = time.time()
	global tread_active
	prev_state = -1
	refreshed = False

	while not rospy.is_shutdown():
		if not tread_active:
			refreshed = True
			continue
		if refreshed:
			refreshed = False
			prev_state = -1
			awal = time.time()
			
		akhir = time.time()
		if akhir - awal < 2:
			state = 0
			if state == prev_state:
				continue
			naik()
			prev_state = 0
			continue
		elif akhir - awal < 4:
			state = 1
			if state == prev_state:
				continue
			turun()
			prev_state = 1
			continue
		elif akhir - awal < 9:
			state = 2
			if state == prev_state:
				continue
			maju()
			prev_state = 2
			continue

		state = 5
		if state == prev_state:
			continue
		finish = kanan()
		prev_state = 5
		if not finish:
			continue

		refreshed = True



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

if __name__=="__main__":

	rospy.init_node("majumundur")

	motor_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=10)
	killswitch_sub = rospy.Subscriber("kill_switch", Int16, killcallback, queue_size=10)
	compass_sub = rospy.Subscriber("/mavros/global_position/compass_hdg",Float64, belok, queue_size=10)
	
	release()
	# tread = threading.Thread(target=naikturun)

	sleep(2)
	start()
	sleep(2)
	tread = threading.Thread(target=naikturun)
	tread.start()
	rospy.spin()

