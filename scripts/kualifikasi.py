#!/usr/bin/env python

import ms5837
import time
import rospy

sensor = ms5837.MS5837_02BA(1) # Default I2C bus is 1 (Raspberry Pi 3)

# inisialisasi
if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)

while not rospy.is_shutdown():
        if sensor.read():
                print("P: %0.1f") % (sensor.pressure()) # dalam mbar

                if(sensor.pressure() < 50): # kalo belom di kedalaman 50 cm
                    # nyelem 
                else:
                    # maju beberapa detik terus mati
        else:
                print "Sensor read failed!"
                exit(1)