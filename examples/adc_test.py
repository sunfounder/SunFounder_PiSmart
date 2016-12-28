#!/usr/bin/env python
'''
**********************************************************************
* Filename    : analog_test.py
* Description : analog port test  
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
**********************************************************************
'''
from pismart.adc import ADC
import time

A0 = ADC(0)
A0.DEBUG = "error"

def setup():
	print '''\
	===================================================="
	|                 Analog port 0 test               |"
	|--------------------------------------------------|"
	|      Potentionmeter  connect to analog 0         |"
	|                                                  |"
	|                  Read analog value               |"
	|                                                  |"
	|                                        SunFounder|"
	===================================================="
	'''
	time.sleep(2)

def main():
	while True:
		print "A0 = %s" % A0.read()
		time.sleep(0.5)

def destroy():
	A0.end()

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
	
