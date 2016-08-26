#!/usr/bin/env python
'''
**********************************************************************
* Filename    : speaker_test.py
* Description : speaker test
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-08-09  Update debug settings
**********************************************************************
'''
from pirobot import PiRobot
import pygame
import time

p = PiRobot()
p.DEBUG = True
p.volume = 100
p.speaker_switch(1)

def setup():
	print "|=====================================================|"
	print "|                   Speaker test                      |"
	print "|-----------------------------------------------------|"
	print "|                                                     |"
	print "|                    Play music                       |"
	print "|                                                     |"
	print "|                                           SunFounder|"
	print "|=====================================================|"


def main():
	pygame.mixer.init()
	pygame.mixer.music.load('my_favpte_things.mp3')
	pygame.mixer.music.play()

	while True:
		time.sleep(1)

def destroy():
	p.speaker_switch(0)

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()	
