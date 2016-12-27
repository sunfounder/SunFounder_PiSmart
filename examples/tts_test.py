#!/usr/bin/env python
'''
**********************************************************************
* Filename    : tts_test.py
* Description : tts test
* Author      : Dream
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-08-09: Update debug setting
**********************************************************************
'''
from pismart.pismart import PiSmart
from pismart.tts import TTS

global string
string = ''

p = PiSmart()
p.DEBUG = True
p.speaker_volume = 100

tts = TTS('pico')

def setup():
    print "===================================================="
    print "|                     TTS test                     |"
    print "|--------------------------------------------------|"
    print "|                                                  |"
    print "|               Speak what you input               |"
    print "|                                                  |"
    print "|                                        SunFounder|"
    print "===================================================="
    p.speaker_switch(1)
    greeting = 'Hello, SunFounder'
    tts.say = greeting

def main():
    global string
    while True:
        string = raw_input("say:")
        tts.say = string

def destroy():
    p.speaker_switch(0)
    tts.end()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
