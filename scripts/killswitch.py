#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Int16

# Pin Definitions
input_pin = 18  # BCM pin 18, BOARD pin 12

def main():
    prev_value = None
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set pin as an input pin
    print("Starting demo now! Press CTRL+C to exit")
    while not rospy.is_shutdown():
        # GPIO.cleanup()
        # GPIO.wait_for_edge(input_pin, GPIO.FALLING)
        value = GPIO.input(input_pin)
        # print(value)
        if value == GPIO.HIGH:
            # print("HIGH")
            print (value)
            nilai = 1
            switch_publisher.publish(nilai)
        else:
            # print("LOW")
            print (value)
            nilai = 0
            switch_publisher.publish(nilai)

if __name__ == '__main__':
    rospy.init_node("killswitch")
    switch_publisher = rospy.Publisher("kill_switch", Int16, queue_size=8)
    prev_value = None


    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin
    print("Starting demo now! Press CTRL+C to exit")
    try:
        while not rospy.is_shutdown():
            value = GPIO.input(input_pin)
            if value == GPIO.HIGH:
                value_str = "HIGH"
                # print(value)
                switch_publisher.publish(value)
            else:
                value_str = "LOW"
                # print(value)
                switch_publisher.publish(value)
    finally:
        GPIO.cleanup()
