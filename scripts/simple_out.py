#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import rospy

# Pin Definitions
output_pin = 18  # BOARD pin 12, BCM pin 18

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BCM)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)

    curr_value = GPIO.HIGH
    while not rospy.is_shutdown():
        # Toggle the output every second
        GPIO.output(output_pin, curr_value)

    GPIO.output(output_pin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    rospy.init_node("led")
    main()
