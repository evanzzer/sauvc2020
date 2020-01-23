#!/usr/bin/env python

import ms5837

sensor = ms5837.MS5837_02BA(1)

if not sensor.init():
        print("sensor gabisa")
        exit(1)

while True:
    if sensor.read():
        print("P: %0.1f") % (sensor.pressure())
    else:
        print("SENSOR GAKEBACA")
