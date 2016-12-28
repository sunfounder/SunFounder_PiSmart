#!/usr/bin/python

import time
import math
import RPi.GPIO as GPIO
import os
import commands
import tempfile
import subprocess
import sys
import pismart
from distutils.spawn import find_executable


DIGITAL_CHANNEL = [17, 18, 27, 22, 23, 24, 25, 4]   # wiringPi pin 0~7 -> BCM GPIO


def _write_data(reg, value):
    self.bus.write_byte_data(PWM_ADDRESS, reg, value)
    return -1

def _write_file(filename, str_value):
    fp = open(filename, "w")
    fp.write(str_value)
    fp.close()
    
def _read_file(filename):
    fp = open(filename, "r")
    value = fp.readline()
    fp.close()
    return value

def _test_mode():
    import test
    try:
        test.main()
    except KeyboardInterrupt:
        test.pismart.end()

def main_setup():
    global usage_dic, p
    usage_dic = {
        'basic'          :'',
        'speaker_volume' :'',
        'speaker_volume' :'',
        'motor_switch'   :'',
        'servo_switch'   :'',
        'speaker_switch' :'',
        'power_type'     :'',
        'get'            :'',
        'test'           :'',
        'all'            :'',
    }
    usage_dic['basic']          = \
          'Usage:\n' \
        + '  pismart [option] [control]\n\n' \
        + 'Options:\n' \
        + '    speaker_volume    Control the volume for speaker\n' \
        + '    capture_volume    Control the volume for microphone\n' \
        + '    motor_switch      Switch for motor\n' \
        + '    servo_switch      Switch for servo\n' \
        + '    speaker_switch    Switch for speaker\n' \
        + '    power_type        Change power type for alarm\n' \
        + '    get               Get informations you want\n' \
        + '    test              Run test mode\n'
    usage_dic['speaker_volume'] = \
          'Usage:\n' \
        + '  pismart speaker_volume [volume]\n\n' \
        + 'volume:      Specified a volume in [0, 100]\n\n' \
        + 'Example:\n' \
        + '  pismart speaker_volume 100  # Set speaker volume to 100%\n'
    usage_dic['capture_volume'] = \
          'Usage:\n' \
        + '  pismart capture_volume [volume]\n\n' \
        + 'volume:      Specified a volume in [0, 100]\n\n' \
        + 'Example:\n' \
        + '  pismart capture_volume 100  # Set capture volume to 100%\n'
    usage_dic['motor_switch']   = \
          'Usage:\n' \
        + '  pismart motor_switch [on/off]\n\n' \
        + 'on/off:      Turn the motor switch on/off with 1/0\n\n' \
        + 'Example:\n' \
        + '  pismart motor_switch 1  # Turn the motor switch on\n'
    usage_dic['servo_switch']   = \
          'Usage:\n' \
        + '  pismart servo_switch [on/off]\n\n' \
        + 'on/off:      Turn the servo switch on/off with 1/0\n\n' \
        + 'Example:\n' \
        + '  pismart servo_switch 1  # Turn the servo switch on\n'
    usage_dic['pwm_switch']   = \
          'Usage:\n' \
        + '  pismart pwm_switch [on/off]\n\n' \
        + 'on/off:      Turn the pwm switch on/off with 1/0\n\n' \
        + 'Example:\n' \
        + '  pismart pwm_switch 1  # Turn the pwm switch on\n'
    usage_dic['speaker_switch'] = \
          'Usage:\n' \
        + '  pismart speaker_switch [on/off]\n\n' \
        + 'on/off:      Turn the speaker switch on/off with 1/0\n\n' \
        + 'Example:\n' \
        + '  pismart speaker_switch 1  # Turn the speaker switch on\n'
    usage_dic['power_type']     = \
          'Usage:\n' \
        + '  pismart power_type [type]\n\n' \
        + 'type:      Specified a power type in 2S/3S/DC, indicate 2S/3S Li-po battery or DC power\n\n' \
        + 'Example:\n' \
        + '  pismart power_type 2S  # Specified the power type as 2S\n'
    usage_dic['get']            = \
          'Usage:\n' \
        + '  pismart get [info]\n\n' \
        + 'info:      Specified an information.\n\n' \
        + 'Avalible informations: \n' \
        + '  voltage      Get power voltage\n' \
        + 'Example:\n' \
        + '  pismart get voltage  # Get current power voltage\n'
    usage_dic['test']            = \
          'Usage:\n'\
        + '  pismart test mode # Run test mode\n\n' \
        + 'Example:\n' \
        + '  pismart test mode # Run test mode\n'
    usage_dic['all']            = \
          usage_dic['basic'] \
        + usage_dic['speaker_volume'] \
        + usage_dic['capture_volume'] \
        + usage_dic['motor_switch'] \
        + usage_dic['servo_switch'] \
        + usage_dic['speaker_switch'] \
        + usage_dic['power_type'] \
        + usage_dic['get'] \
        + usage_dic['test']
    p = pismart.PiSmart() 

def usage(opt = 'basic'):
    print usage_dic[opt]
    quit()

def check_command():
    option = ''
    argv_len = len(sys.argv)

    if argv_len < 2:
        usage()
    else:
        option = sys.argv[1]

    if argv_len < 3:
        control = None
    else:
        control = sys.argv[2]
    return option, control

def on_off_handle(on_off):
    if isinstant(on_off, str):
        on_off=on_off.lower()
        if on_off == 'on':
            on_off = 1
        elif on_off == 'off':
            on_off = 0
        else:
            return false
    else:
        try:
            on_off = int(control)
        except:
            return false
    return on_off

def main():
    main_setup()
    option, control = check_command()

    if option in ['help', 'h']:
        if option == None:
            usage()
        else:
            if control in usage_dic:
                usage(control)
            else:
                usage()
    elif option == 'speaker_volume':
        try:
            control = int(control)
        except:
            usage("speaker_volume")
        if control not in range(0, 101):
            usage("speaker_volume")
        p.volume = control
    elif option == 'capture_volume':
        try:
            control = int(control)
        except:
            usage("capture_volume")
        if control not in range(0, 101):
            usage("capture_volume")
        p.capture_volume = control
    elif option == 'motor_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage("motor_switch")
        p.motor_switch(control)
    elif option == 'speaker_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage("speaker_switch")
        p.speaker_switch(control)
    elif option == 'servo_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage("servo_switch")
        p.servo_switch(control)
    elif option == 'pwm_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage("pwm_switch")
        p.pwm_switch(control)
    elif option == 'power_type':
        try:
            control = int(control)
        except:
            usage("capture_volume")
        if control not in ['2S', '3S', 'DC']:
            usage("power_type")
        p.power_type = control
    elif option == 'get':
        if control == 'voltage':
            print "Power voltage now is: %sV"%p.power_voltage
        else:
            usage("get")
    elif option == 'test':
        if control == 'mode':
            _test_mode()
        else:
            usage("test")
    else:
        print 'Option Error'
        usage()
        
