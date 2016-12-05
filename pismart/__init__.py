#!/usr/bin/python

import time
import math
import RPi.GPIO as GPIO
import os
import commands
import tempfile
import subprocess
import sys
from distutils.spawn import find_executable


CHANNEL0_HIGH       = 0x10
CHANNEL0_LOW        = 0x11
CHANNEL1_HIGH       = 0x12
CHANNEL1_LOW        = 0x13
CHANNEL2_HIGH       = 0x14
CHANNEL2_LOW        = 0x15
CHANNEL3_HIGH       = 0x16
CHANNEL3_LOW        = 0x17
CHANNEL4_HIGH       = 0x18
CHANNEL4_LOW        = 0x19
POWER_VOLTAGE_HIGH  = 0x1a
POWER_VOLTAGE_LOW   = 0x1b

ANALOG_CHANNEL = [CHANNEL0_HIGH, CHANNEL1_HIGH, CHANNEL2_HIGH, CHANNEL3_HIGH, CHANNEL4_HIGH, POWER_VOLTAGE_HIGH]
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

class PiSmart(_Basic_class):

    _class_name = 'PiSmart'
    
    ON  = 1
    OFF = 0

    SERVO_POWER_OFF     = 0x20
    SERVO_POWER_ON      = 0x21
    SPEAKER_POWER_OFF   = 0x22
    SPEAKER_POWER_ON    = 0x23
    MOTOR_POWER_OFF     = 0x24
    MOTOR_POWER_ON      = 0x25
    SET_POWER_DC        = 0X26  # power_type = 0, DC power
    SET_POWER_2S        = 0X27  # power_type = 1, Li-po battery 2s
    SET_POWER_3S        = 0X28  # power_type = 2, Li-po battery 3s

    SYS_ADDRESS = 0x10

    def __init__(self):
        self._volume = 70
        self._power_type = '2S'
        self.power_type = self._power_type
        self.logger_setup()
        self._debug('Init PiSmart object complete')

    @staticmethod
    def _write_sys_byte(value):
        self.bus.write_byte(self.SYS_ADDRESS, value)
        return -1

    @staticmethod
    def _read_sys_byte(reg, delay=0):
        #number = self.bus.read_word_data(self.SYS_ADDRESS, reg)
        self.bus.write_byte(self.SYS_ADDRESS, reg)
        #print 'reg:',hex(reg)
        if delay != 0:
            time.sleep(delay)
        number = self.bus.read_byte(self.SYS_ADDRESS)
        if delay != 0:
            time.sleep(delay)
        #print 'read:',number
        return number

    def servo_switch(self, on_off):
        self.pwm_switch(on_off)

    def pwm_switch(self, on_off):
        if on_off not in (0, 1):
            raise ValueError ("On_off set must be .ON(1) or .OFF(0), not \"{0}\".".format(on_off))
        if on_off == 1:
            _write_sys_byte(self.SERVO_POWER_ON)
            self._debug('Servo switch ON')
        else:
            _write_sys_byte(self.SERVO_POWER_OFF)
            self._debug('Servo switch OFF')

    def motor_switch(self, on_off):
        if on_off not in (0, 1):
            raise ValueError ("On_off set must be .ON(1) or .OFF(0), not \"{0}\".".format(on_off))
        if on_off == 1:
            _write_sys_byte(self.MOTOR_POWER_ON)
            self._debug('Motor switch ON')
        else:
            _write_sys_byte(self.MOTOR_POWER_OFF)
            self._debug('Motor switch OFF')

    def speaker_switch(self, on_off):
        if on_off not in (0, 1):
            raise ValueError ("On_off set must in .ON(1) or .OFF(0), not \"{0}\".".format(on_off))
        if on_off == 1:
            _write_sys_byte(self.SPEAKER_POWER_ON)
            self._debug('Speaker switch ON')
        else:
            _write_sys_byte(self.SPEAKER_POWER_OFF)
            self._debug('Speaker switch OFF')

    @property
    def power_type(self):
        return self._power_type
    
    @power_type.setter
    def power_type(self, power_type):
        if power_type not in ['2S', '3S', 'DC']:
            raise ValueError ('Power type only support: "2S", "3S" Li-po battery or "DC" power, not \"{0}\".'.format(power_type))
        else:
            self._power_type = power_type
            if power_type == '2S':
                _write_sys_byte(SET_POWER_2S)
                self._debug('Set power type to 2S Li-po battery')
            elif power_type == '3S':
                _write_sys_byte(SET_POWER_3S)
                self._debug('Set power type to 3S Li-po battery')
            elif power_type == 'DC':
                _write_sys_byte(SET_POWER_DC)
                self._debug('Set power type to DC power')

    '''
        def get_cpu_temperature(self):
            raw_cpu_temperature = _read_file("/sys/class/thermal/thermal_zone0/temp")
            cpu_temperature = float(raw_cpu_temperature)/1000
            cpu_temperature = 'Cpu temperature : ' + str(cpu_temperature)
            return cpu_temperature

        def get_gpu_temperature(self):
            raw_gpu_temperature = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' )
            gpu_temperature = float(raw_gpu_temperature.replace( 'temp=', '' ).replace( '\'C', '' ))
            gpu_temperature = 'Gpu temperature : ' + str(gpu_temperature)
            return gpu_temperature

        def get_ram_info(self):
            p = os.popen('free')
            i = 0
            while 1:
                i = i + 1
                line = p.readline()
                if i==2:
                    return line.split()[1:4]

        def get_ram_total(self):
            ram_status = _get_ram_info()
            ram_total = 'Ram total : %s' % round(int(ram_status[0]) / 1000,1)
            return ram_total

        def get_ram_used(self):
            ram_status = _get_ram_info()
            ram_used = 'Ram used : %s' % round(int(ram_status[1]) / 1000,1)
            return ram_used

        def get_disk_space(self):
            p = os.popen("df -h /")
            i = 0
            while 1:
                i = i +1
                line = p.readline()
                if i==2:
                    return line.split()[1:5]

        def get_disk_total(self):
            disk_status = _get_disk_space()
            disk_total = 'Disk total : %s' % disk_status[0][:-1]
            return disk_total

        def get_disk_used(self):
            disk_status = _get_disk_space()
            disk_used = 'Disk used : %s' % disk_status[1][:-1]
            return disk_used
                                   
        def get_cpu_usage(self):

            return str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
    '''

    def read_analog(self, channel, ignore_false=True, delay=0.000001):
        value_return = 0
        if channel not in range(0, 6):
            raise ValueError ("Analog channel should be in [0, 5], not \"{0}\".".format(channel))
        value = [0, 0]
        try:
            value[0] = _read_sys_byte(ANALOG_CHANNEL[channel], delay=delay)
            self._debug('Read high value = 0x%2X' % value[0])
            value[1] = _read_sys_byte(ANALOG_CHANNEL[channel]+1, delay=delay)
            self._debug('Read low value = 0x%2X' % value[1])
        except Exception, e:
            if not ignore_false:
                print e 
        value_return = (value[0] << 8) + (value[1])
        self._debug('Read value = %d ' % value_return)
        return value_return

    def read_battery(self):
        A7_value = self.read_analog(5)
        A7_volt = float(A7_value) / 1024 * 5
        battery_volt = round(A7_volt * 14.7 / 4.7, 2)
        self._debug('Read battery: %d V' % battery_volt)
        return battery_volt

    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, value):
        if value not in range(0, 101):
            raise ValueError ("Volume should be in [0, 100], not \"{0}\".".format(value))
        self._volume = _map(value, 0, 100, -10239, 400)
        cmd = "sudo amixer cset numid=1 -- %d" % self._volume
        self.run_command(cmd)
        return 0
    
    @property
    def capture_volume(self):
        return self._capture_volume

    @capture_volume.setter
    def capture_volume(self, value):
        capture_volume_id = self._get_capture_volume_id()
        if value not in range(0, 101):
            raise ValueError ("Volume should be in [0, 100], not \"{0}\".".format(value))
        self._capture_volume = _map(value, 0, 100, 0, 16)
        cmd = "sudo amixer -c 1 cset numid=%s -- %d" % (capture_volume_id, self._capture_volume)
        self.run_command(cmd)
        return 0

    def _get_capture_volume_id(self):
        all_controls = self.run_command("sudo amixer -c 1 controls")
        all_controls = all_controls.split('\n')
        capture_volume = ''
        capture_volume_id = ''
        for line in all_controls:
            if 'Mic Capture Volume' in line:
                capture_volume = line
        capture_volume=capture_volume.split(',')
        for variable in capture_volume:
            if 'numid' in variable:
                capture_volume_id = variable
        capture_volume_id = capture_volume_id.split('=')[1]
        return int(capture_volume_id)


def main_setup():
    global usage_dic
    usage_dic = {
        'basic'          :'',
        'speaker_volume' :'',
        'speaker_volume' :'',
        'motor_switch'   :'',
        'servo_switch'   :'',
        'speaker_switch' :'',
        'power_type'     :'',
        'get'            :'',
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
        + '    get               Get informations you want\n'
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
    usage_dic['all']            = \
          usage_dic['basic'] \
        + usage_dic['speaker_volume'] \
        + usage_dic['capture_volume'] \
        + usage_dic['motor_switch'] \
        + usage_dic['servo_switch'] \
        + usage_dic['speaker_switch'] \
        + usage_dic['power_type'] \
        + usage_dic['get']
    p = PiSmart() 

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
    return option

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
    option = check_command()

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
            usage(speaker_volume)
        if control not in range(0, 101):
            usage(speaker_volume)
        p.volume = control
    elif option == 'capture_volume':
        try:
            control = int(control)
        except:
            usage(capture_volume)
        if control not in range(0, 101):
            usage(capture_volume)
        p.capture_volume = control
    elif option == 'motor_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage(motor_switch)
        p.motor_switch(control)
    elif option == 'speaker_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage(speaker_switch)
        p.speaker_switch(control)
    elif option == 'servo_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage(servo_switch)
        p.servo_switch(control)
    elif option == 'pwm_switch':
        control = on_off_handle(contorl)
        if control not in [0, 1]:
            usage(pwm_switch)
        p.pwm_switch(control)
    elif option == 'power_type':
        if control not in ['2S', '3S', 'DC']:
            usage(power_type)
        p.power_type = control
    elif option == 'get':
        if control == 'voltage':
            print "Power voltage now is:", p.read_battery()
        else:
            usage(get)
    else:
        print 'Option Error'
        usage()
        
