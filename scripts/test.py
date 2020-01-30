#!/usr/bin/env python

import time
import rospy
from datetime import datetime
import ms5837

sensor = ms5837.MS5837_02BA(1)

while not rospy.is_shutdown():
	if sensor.read():
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		file1 = open("data_press.txt", "a")
		file1.write("waktu: " + current_time + str(sensor.pressure()) + "\n")
		file1.close()
