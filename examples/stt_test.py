#!/usr/bin/env python
'''
**********************************************************************
* Filename    : speech_recognition_test.py
* Description : an simple script to test the speech recognition function
* Author      : Cavon
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-08-01    New release
*               Cavon    2016-08-24    Update debug setting
**********************************************************************
'''
from pismart.pismart import PiSmart
from pismart.stt import STT
from pismart.tts import TTS

p = PiSmart()
sr = STT('sample', name_calling=True, timeout=10.0, dictionary_update=True)
sr.DEBUG = True
p.speaker_switch(1)

pico = TTS('pico')

def setup():
	print '|==================================================|'
	print '|             Speech Recognition Test              |'
	print '|--------------------------------------------------|'
	print '|    Say my Name "pirobot", and wait till I returns|'
	print '| "Hello there", ask me "How are you", and I will  |'
	print '| response you "I am fine thank you"               |'
	print '|    See the manuel for detials.                   |'
	print '|                                                  |'
	print '|                                        SunFounder|'
	print '|==================================================|'

def main():
	last_result = 'None'

	while True:
		sr.recognize()
		result = sr.result
		if result != last_result and result != '':
			print "=============================="
			print result
			print "=============================="
			if result == '__NAME__':
				pico.say('Hello there')
			else:
				pico.say(result)
			last_result = result

def destroy():
	p.speaker_switch(0)
	sr.end()
	pico.end()

if __name__ == '__main__':
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
