#!/usr/bin/env python
'''
**********************************************************************
* Filename    : analog_test.py
* Description : analog port test  
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-08-10 Change debug setting
*               Cavon    2016-08-23 Change I/O port
**********************************************************************
'''
from pismart import PiSmart
import time

p = PiSmart()
p.DEBUG = True

def setup():
	print "===================================================="
	print "|                 Analog port 0 test               |"
	print "|--------------------------------------------------|"
	print "|      Potentionmeter  connect to analog 0         |"
	print "|                                                  |"
	print "|                  Read analog value               |"
	print "|                                                  |"
	print "|                                        SunFounder|"
	print "===================================================="
	time.sleep(2)

def main():
	while True:
		A0 = p.read_analog(0)
		print A0
		time.sleep(0.5)

def destroy():
	pass

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
	
