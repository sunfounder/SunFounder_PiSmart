#!/usr/bin/env python
'''
**********************************************************************
* Filename    : motor_test.py
* Description : motor port test
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-08-09: Update debug_settings
**********************************************************************
'''
from pirobot import PiRobot, Motor
import time
import RPi.GPIO

p = PiRobot()
motorA = Motor("Motor A")
motorB = Motor("Motor B")

p.DEBUG = True
motorA.DEBUG = True
motorB.DEBUG = True
p.motor_switch(1)

last_speed = 0

def setup():
	print "|==================================================|"
	print "|                 Motor port test                  |"
	print "|--------------------------------------------------|"
	print "|     Motors connect to Motor A and Motor B port   |"
	print "|                                                  |"
	print "|           Input value and motors work            |"
	print "|                                                  |"
	print "|                                        SunFounder|"
	print "|==================================================|"

def main():
	global last_speed

	while True:

		speed = input("input: ")

		if speed != last_speed:
			
			motorA.forward(speed)
			motorB.forward(speed)

			last_speed = speed

def destroy():
	motorA.stop()
	motorB.stop()
	p.motor_switch(0)
	RPi.GPIO.cleanup()

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
