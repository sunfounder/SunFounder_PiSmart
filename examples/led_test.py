#!/usr/bin/env python
'''
**********************************************************************
* Filename    : led_test.py
* Description : led test
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-07-28 New version
*               Cavon    2016-08-23 Update set debug
**********************************************************************
'''
from pismart.led import LED
import time

leds = LED()
leds.DEBUG = 'debug'

LED_MAX = 100
LED_MIN = 10

def setup():
	print "|=====================================================|"
	print "|                   LED Ring test                     |"
	print "|-----------------------------------------------------|"
	print "|                                                     |"
	print "|              Breath Blue leds breath                |"
	print "|                                                     |"
	print "|                                           SunFounder|"
	print "|=====================================================|"
	time.sleep(2)

def main():
	while True:
		for x in xrange(LED_MIN, LED_MAX, 1):
			leds.brightness = x
			time.sleep(0.01)
		for x in xrange(LED_MAX, LED_MIN, -1):
			leds.brightness = x
			time.sleep(0.015)

def destroy():
	leds.off()

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
