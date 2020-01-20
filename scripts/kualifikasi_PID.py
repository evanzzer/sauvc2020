#!/usr/bin/env python

import ms5837
import time
import rospy
from std_msgs.msg import Float64

sensor = ms5837.MS5837_02BA(1) # Default I2C bus is 1 (Raspberry Pi 3)

if __name__ == '__main__':
    rospy.init_node('kualifikasi_PID', anonymous=True)

    state_publisher = rospy.Publisher("kualifikasi/state", Float64, queue_size=8)
    # controleffort_subscriber = rospy.Subscriber("control_effort", Float64, control_effort_callback)

    # inisialisasi
    if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)

    while not rospy.is_shutdown():
        if sensor.read():
            state = Float64()
            state.data = sensor.pressure()
            state_publisher(state)
            # print("P: %0.1f") % (sensor.pressure()) # dalam mbar
        else:
            print "Sensor read failed!"
            exit(1)