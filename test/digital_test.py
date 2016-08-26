#!/usr/bin/env python
'''
**********************************************************************
* Filename 	 : digital_test.py
* Description: digital port test  
* Author 	 : Dream
* E-mail 	 : service@sunfounder.com
* Website 	 : www.sunfounder.com
* Update 	 : Dream    2016-07-28
* Detail	 : New version
**********************************************************************
'''
import RPi.GPIO as GPIO
import time

def setup():
	print "|==================================================|"
	print "|              Analog port 1 test                  |"
	print "|--------------------------------------------------|"
	print "|             Led connect to digital 1             |"
	print "|                                                  |"
	print "|                    Blink led                     |"
	print "|                                                  |"
	print "|                                        SunFounder|"
	print "|==================================================|"
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(1, GPIO.OUT)

def main():
	while True:
		print "led on"
		GPIO.output(1, 0)
		time.sleep(0.3)
		print "led off"
		GPIO.output(1, 1)
		time.sleep(0.3)

def destroy():
	GPIO.cleanup(1)

if __name__ == '__main__':
			try:
				setup()
				main()
			except KeyboardInterrupt:
				destroy()
					
