#!/usr/bin/env python
'''
**********************************************************************
* Filename 	 : digital_test.py
* Description: digital port test  
* Author 	 : Dream
* E-mail 	 : service@sunfounder.com
* Website 	 : www.sunfounder.com
* Update 	 : Dream 2016-07-28  New version
*			   Dream 2016-12-21  All digital channel input/output test   
**********************************************************************
'''
import RPi.GPIO as GPIO
import time

chan_list = [17, 18, 27, 22, 23, 24, 25, 4]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup():
	global option
	print "|==================================================|"
	print "|                Digital port test                 |"
	print "|--------------------------------------------------|"
	print "|         All digital channel output/input         |"
	print "|                choose one to test                |"
	print "|                 1. output                        |"
	print "|                 2. input                         |"
	print "|                                        SunFounder|"
	print "|==================================================|"
	option = raw_input ("Test what:") 

def main():
	global option
	while True:
		if option == "1":
			GPIO.setup(chan_list, GPIO.OUT)
			while True:
				print "digital output: 1 1 1 1 1 1 1 1 "
				GPIO.output(chan_list, 1)
				time.sleep(0.3)
				print "digital output: 0 0 0 0 0 0 0 0 "
				GPIO.output(chan_list, 0)
				time.sleep(0.3)
		elif option == "2":
			GPIO.setup(chan_list, GPIO.IN)
			while True:
				value = []
				for channel in range(0, 8):
					value.append(GPIO.input(chan_list[channel]))
				print "digital read: %s "%value
				time.sleep(0.3)
		else:
			print "input error option \n"
			setup()

def destroy():
	GPIO.setup(chan_list, GPIO.IN)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()
					
