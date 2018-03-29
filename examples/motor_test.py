#!/usr/bin/env python
'''
**********************************************************************
* Filename    : motor_test.py
* Description : motor port test
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-08-09: Update debug_settings
*               Cavon    2016-09-27: Add " " cmd to reverse
**********************************************************************
'''
from pismart.pismart import PiSmart
from pismart.motor import Motor

p = PiSmart()
motorA = Motor("MotorA")
motorB = Motor("MotorB")

p.DEBUG = True
motorA.DEBUG = True
motorB.DEBUG = True
p.motor_switch(1)

def setup():
	print "|==================================================|"
	print "|                 Motor port test                  |"
	print "|--------------------------------------------------|"
	print "|     Motors connect to Motor A and Motor B port   |"
	print "|                                                  |"
	print "|      Input value(0, 100) to set motors speed     |"
	print "|        Input " "(space) to reverse motors        |"
	print "|                                                  |"
	print "|                                        SunFounder|"
	print "|==================================================|"

def main():
	direction = True
	speed = 0
	while True:
		value = raw_input("input: ")
		
		if value == " ":
			direction = not direction
		else:
			try:
				speed = int(value)
			except:
				print "wrong input, input value: 0~100"
		if direction:
			motorA.forward(speed)
			motorB.forward(speed)
			print "direction: Forward"
		else:
			motorA.backward(speed)
			motorB.backward(speed)
			print "direction: Backward"

def destroy():
	motorA.stop()
	motorB.stop()
	p.motor_switch(0)

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
