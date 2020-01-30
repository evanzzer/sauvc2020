#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
# import rospy

# Pin Definitions
input_pin = 18  # BOARD pin 12, BCM pin 18

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BCM)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(input_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)

    curr_value = GPIO.HIGH
    while True:
        # Toggle the output every second
        a = GPIO.input(input_pin)
        print(a)
    # GPIO.output(output_pin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    # rospy.init_node("led")
    main()
