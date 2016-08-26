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
from pirobot import LED
import time

blue_leds = LED(LED.BLUE)
blue_leds.DEBUG = True

red_leds  = LED(LED.RED)
red_leds.DEBUG = True

def setup():
	print "|=====================================================|"
	print "|                     LED test                        |"
	print "|-----------------------------------------------------|"
	print "|                                                     |"
	print "|         Blue leds breath and then red leds          |"
	print "|                                                     |"
	print "|                                           SunFounder|"
	print "|=====================================================|"

def main():
	while True:
		for x in xrange(1,3):
			for x in xrange(10, 60, 2):
				blue_leds.brightness = x
				time.sleep(0.03)
			for x in xrange(60,10, -1):
				blue_leds.brightness = x
				time.sleep(0.05)
		blue_leds.off()

		for x in xrange(1,3):
			for x in xrange(10, 60, 2):
				red_leds.brightness = x
				time.sleep(0.03)
			for x in xrange(60,10, -1):
				red_leds.brightness = x
				time.sleep(0.05)
		red_leds.off()

def destroy():
	red_leds.off()
	blue_leds.off()

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
