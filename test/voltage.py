#!/usr/bin/env python
'''
**********************************************************************
* Filename    : voltage_test.py
* Description : voltage test
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-07-28  New version
**********************************************************************
'''
from pirobot import PiRobot
import time
import os

p = PiRobot()
p.DEBUG = False

while True:
	print p.read_battery()

	time.sleep(1)
