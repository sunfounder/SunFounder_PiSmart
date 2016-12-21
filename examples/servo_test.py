#!/usr/bin/env python
'''
**********************************************************************
* Filename    : servo_test.py
* Description : servo port test  
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-07-28  New version
*               Cavon    2016-08-23  Update setup debug
**********************************************************************
'''
from pismart.servo import Servo
from pismart.pismart import PiSmart
import time

my_servo = Servo(0)
my_servo.DEBUG = "debug"

p = PiSmart()
p.DEBUG = "debug"

p.servo_switch(1)    #on = 1 ; off = 0
time.sleep(0.3)

def setup():
	print "===================================================="
	print "|                 Servo port test                  |"
	print "|--------------------------------------------------|"
	print "|          Servo connect to servo 0 port           |"
	print "|                                                  |"
	print "|                    Servo work                    |"
	print "|                                                  |"
	print "|                                        SunFounder|"
	print "===================================================="
	time.sleep(2)

def main():
	while True:
		for i in xrange(0,180):
			my_servo.angle = i
			time.sleep(0.01)

		for i in xrange(180,0,-1):
			my_servo.angle = i
			time.sleep(0.01)

def destroy():
	p.servo_switch(0)

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
