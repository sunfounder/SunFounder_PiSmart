#!/usr/bin/python

import smbus
import time
import math
import RPi.GPIO as GPIO
import os
import commands
import tempfile
import subprocess
from distutils.spawn import find_executable

RUNTIME = 1000

_BOX_DIR_= '/home/pi/SunFounder_PiRobot/'

_LED0_ON_L          = 0x06
_LED0_ON_H          = 0x07
_LED0_OFF_L         = 0x08
_LED0_OFF_H         = 0x09

SERVO_POWER_OFF		= 0x20
SERVO_POWER_ON		= 0x21
SPEAKER_POWER_OFF	= 0x22
SPEAKER_POWER_ON	= 0x23
MOTOR_POWER_OFF		= 0x24
MOTOR_POWER_ON		= 0x25
SET_POWER_DC 		= 0X26	# power_type = 0, DC power
SET_POWER_2S 		= 0X27	# power_type = 1, Li-po battery 2s
SET_POWER_3S 		= 0X28	# power_type = 2, Li-po battery 3s

CHANNEL0_HIGH		= 0x10
CHANNEL0_LOW		= 0x11
CHANNEL1_HIGH		= 0x12
CHANNEL1_LOW		= 0x13
CHANNEL2_HIGH		= 0x14
CHANNEL2_LOW		= 0x15
CHANNEL3_HIGH		= 0x16
CHANNEL3_LOW		= 0x17
CHANNEL4_HIGH		= 0x18
CHANNEL4_LOW		= 0x19
POWER_VOLTAGE_HIGH	= 0x1a
POWER_VOLTAGE_LOW	= 0x1b

ANALOG_CHANNEL = [CHANNEL0_HIGH, CHANNEL1_HIGH, CHANNEL2_HIGH, CHANNEL3_HIGH, CHANNEL4_HIGH, POWER_VOLTAGE_HIGH]
DIGITAL_CHANNEL = [17, 18, 27, 22, 23, 24, 25, 4]	# wiringPi pin 0~7 -> BCM GPIO

MOTOR_A = 0
MOTOR_B = 1

ON 	= 1
OFF = 0

PWM_ADDRESS = 0x40
SYS_ADDRESS = 0x10

bus = smbus.SMBus(1)

GPIO.setwarnings(False)

def _map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def _write_sys_byte(value):
	bus.write_byte(SYS_ADDRESS, value)
	return -1
	
def _read_sys_byte(reg, delay=0):
	#number = bus.read_word_data(SYS_ADDRESS, reg)
	bus.write_byte(SYS_ADDRESS, reg)
	#print 'reg:',hex(reg)
	if delay != 0:
		time.sleep(delay)
	number = bus.read_byte(SYS_ADDRESS)
	if delay != 0:
		time.sleep(delay)
	#print 'read:',number
	return number

def _write_data(reg, value):
	bus.write_byte_data(PWM_ADDRESS, reg, value)
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

class _Basic_class(object):

	_class_name = '_Basic_class'
	_DEBUG = False

	def __init__(self):
		pass
		
	@property
	def DEBUG(self):
		return self._DEBUG
	
	@DEBUG.setter
	def DEBUG(self, debug):
		if debug  not in (True, False):
			raise ValueError("Debug value must be True(1) or False(0), \"{0}\" is not bool.".format(debug))	
		else:
			self._DEBUG = debug
			self.debug('Set debug %s' % debug)

	def debug(self, message):
		if self._DEBUG:
			print "DEBUG: pirobot, class %s: %s" % (self._class_name, message)

	def run_command(self, cmd):
		self.debug('Run command: "%s"' % cmd)
		with tempfile.TemporaryFile() as f:
			subprocess.call(cmd, shell=True, stdout=f, stderr=f)
			f.seek(0)
			output = f.read()
			return output

class PiRobot(_Basic_class):

	_class_name = 'PiRobot'

	def __init__(self):
		self._volume = 70
		self._power_type = '2S'
		self.power_type = self._power_type
		self.debug('Init PiRobot object complete')

	def servo_switch(self, on_off):
		if on_off not in (0, 1):
			raise ValueError ("On_off set must be .ON(1) or .OFF(0), not \"{0}\".".format(on_off))
		if on_off == 1:
			_write_sys_byte(SERVO_POWER_ON)
			self.debug('Servo switch ON')
		else:
			_write_sys_byte(SERVO_POWER_OFF)
			self.debug('Servo switch OFF')

	def motor_switch(self, on_off):
		if on_off not in (0, 1):
			raise ValueError ("On_off set must be .ON(1) or .OFF(0), not \"{0}\".".format(on_off))
		if on_off == 1:
			_write_sys_byte(MOTOR_POWER_ON)
			self.debug('Motor switch ON')
		else:
			_write_sys_byte(MOTOR_POWER_OFF)
			self.debug('Motor switch OFF')

	def speaker_switch(self, on_off):
		if on_off not in (0, 1):
			raise ValueError ("On_off set must in .ON(1) or .OFF(0), not \"{0}\".".format(on_off))
		if on_off == 1:
			_write_sys_byte(SPEAKER_POWER_ON)
			self.debug('Speaker switch ON')
		else:
			_write_sys_byte(SPEAKER_POWER_OFF)
			self.debug('Speaker switch OFF')

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
				self.debug('Set power type to 2S Li-po battery')
			elif power_type == '3S':
				_write_sys_byte(SET_POWER_3S)
				self.debug('Set power type to 3S Li-po battery')
			elif power_type == 'DC':
				_write_sys_byte(SET_POWER_DC)
				self.debug('Set power type to DC power')

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
			self.debug('Read high value = 0x%2X' % value[0])
			value[1] = _read_sys_byte(ANALOG_CHANNEL[channel]+1, delay=delay)
			self.debug('Read low value = 0x%2X' % value[1])
		except Exception, e:
			if not ignore_false:
				print e	
		value_return = (value[0] << 8) + (value[1])
		self.debug('Read value = %d ' % value_return)
		return value_return

	def read_battery(self):
		A7_value = self.read_analog(5)
		A7_volt = float(A7_value) / 1024 * 5
		battery_volt = round(A7_volt * 14.7 / 4.7, 2)
		self.debug('Read battery: %d V' % battery_volt)
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
		capture_volume_id = self.get_capture_volume_id()
		if value not in range(0, 101):
			raise ValueError ("Volume should be in [0, 100], not \"{0}\".".format(value))
		self._capture_volume = _map(value, 0, 100, 0, 16)
		cmd = "sudo amixer -c 1 cset numid=%s -- %d" % (capture_volume_id, self._capture_volume)
		self.run_command(cmd)
		return 0

	def get_capture_volume_id(self):
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

class PWM(_Basic_class):
	def __init__(self, channel):
		if channel not in range(0, 16):
			raise ValueError("Servo channel \"{0}\" is not in (0, 15).".format(channel))
		self.channel = channel

	def set_PWM(self, on):
		bus.write_byte_data(PWM_ADDRESS, _LED0_ON_L+4*self.channel, 0)
		bus.write_byte_data(PWM_ADDRESS, _LED0_ON_H+4*self.channel, 0)
		bus.write_byte_data(PWM_ADDRESS, _LED0_OFF_L+4*self.channel, on & 0xFF)
		bus.write_byte_data(PWM_ADDRESS, _LED0_OFF_H+4*self.channel, on >> 8)

class Servo(PWM):
	_MIN_PULSE_WIDTH	= 544
	_MAX_PULSE_WIDTH	= 2400
	_FREQUENCY			= 60

	_class_name = 'Servo'

	def __init__(self, channel, offset=0):
		if channel not in range(0, 8):
			raise ValueError("Servo channel \"{0}\" is not in (0, 7).".format(channel))
		self.channel = channel
		self._offset = offset

	def _angle_to_analog(self, angle):
		pulse_wide   = _map(angle, 0, 180, self._MIN_PULSE_WIDTH, self._MAX_PULSE_WIDTH)
		analog_value = int(float(pulse_wide) / 1000000 * self._FREQUENCY * 4096)
		return analog_value
		
	def turn(self, angle):
		if angle<0 or angle>180:
			raise ValueError("Servo \"{0}\" turn angle \"{1}\" is not in (0, 180).".format(self.channel, angle))		
		value = self._angle_to_analog(angle)
		value += self._offset
		self.set_PWM(value)
		self.debug('Servo turn. channel: [%d] to angle: [%d]' % (self.channel, angle))

	@property
	def offset(self):
		return self._offset
	
	@offset.setter
	def offset(self, value):
		self._offset = value

class LED(PWM):

	RED         = 9
	BLUE        = 8
	BRIGHT      = 60
	RUNING      = 30
	DIMING      = 10
	OFF         = 0
	
	BRIGHT_X = 100			#how long it will be bright 
	SLEEP_TIME  = 0.02

	_class_name = 'LED'

	def __init__(self, channel):
		if channel not in (8, 9):
			raise ValueError ("Led channel should be .RED(9) or .BLUE(8), not \"{0}\".".format(channel))
		self.channel = channel
		self.debug('Init LED channel [%d] complate. (8 = BLUE, 9 = RED)' % self.channel)

	def _get_pwm_from_brightness(self, brightness):
		pwm_value = _map(brightness, 0, 100, 0, 4095)
		return int(pwm_value)
	@property
	def brightness(self):
		return self._brightness
	
	@brightness.setter
	def brightness(self, value):
		if value not in xrange(0, 101):
			raise ValueError ("Brightness set must in [0,100], not \"{0}\".".format(value))
		self._brightness = value
		pwm_value = self._get_pwm_from_brightness(self._brightness)
		self.set_PWM(pwm_value)
		self.debug('Set LED [%d] to [%d].' % (self.channel, self._brightness))

	def off(self):
		pwm_value = self._get_pwm_from_brightness(self.OFF)
		self.set_PWM(self.OFF)
		self.debug('Set LED [%d] OFF.' % self.channel)

class Motor(PWM):
	MOTOR_CHANNEL = {10:5, 11:6}

	OFF = 0

	_class_name = 'Motor'

	def __init__(self, channel, forward=0):
		if channel == 'Motor A':
			channel = 0
		if channel == 'Motor B':
			channel = 1
		if channel not in (0, 1):
			raise ValueError ("Motor channel should be .MOTOR_A(0) or .MOTOR_B(1), not \"{0}\".".format(channel))
		self.channel = channel + 10

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.MOTOR_CHANNEL[self.channel], GPIO.OUT)
		if forward not in (0, 1):
			raise ValueError ("Forward direction should be 0 or 1, not \"{0}\".".format(forward))
		self._forward_direction = forward
		self._backward_direction = (forward + 1) & 1
		self.debug('Init motor channel [%d] complate. (10 = MOTOR_A, 11 = MOTOR_B)' % self.channel)

	def _speed_to_analog(self, speed):
		pwm_value = _map(speed, 0, 100, 0, 4095)
		self.debug('  speed: %d,  ->   pwm_value: %d' % (speed, pwm_value))
		return int(pwm_value)

	@property
	def forward_direction(self):
		return self._forward_direction
	
	@forward_direction.setter
	def forward_direction(self, value):
		self._forward_direction = value
		self._backward_direction = (value + 1) & 1

	def forward(self, speed=50):
		if speed not in xrange(0, 101):
			raise ValueError ("Motor forward speed should be in (0, 100) not \"{0}\".".format(speed))
		analog_value = self._speed_to_analog(speed)
		self.set_PWM(analog_value)
		GPIO.output(self.MOTOR_CHANNEL[self.channel], self._forward_direction)
		self.debug('Motor forward direction channel[%d], pwm channel [%d]' % (self.MOTOR_CHANNEL[self.channel], self.channel))

	def backward(self, speed=50):
		if speed not in xrange(0, 101):
			raise ValueError ("Motor backward speed should be in (0, 100) not \"{0}\".".format(speed))
		analog_value = self._speed_to_analog(speed)
		self.set_PWM(analog_value)
		GPIO.output(self.MOTOR_CHANNEL[self.channel], self._backward_direction)
		self.debug('Motor backward, direction channel [%d], pwm channel [%d]' % (self.MOTOR_CHANNEL[self.channel], self.channel))

	def stop(self):
		self.set_PWM(self.OFF)
		GPIO.output(self.MOTOR_CHANNEL[self.channel], 0)
		self.debug('Motor stop, direction channel [%d], pwm channel [%d]' % (self.MOTOR_CHANNEL[self.channel], self.channel))

'''	
class DS18B20(_Basic_class):
	#need to enable w1 interface and add 1-wire module 
	#sudo nano /boot/config.txt
	#	add  this content :
	#		dtoverlay = w1-gpio 
	#	sudo nano /etc/modules
	#	add following contents:
	#		w1-gpio
	#		w1-therm
	def __init__(self):
		self._ds18b20 = ''
		self.C = 0
		self.F = 1
		self.run_command('sudo modprobe w1-gpio')
		self.run_command('sudo modprobe w1-therm')
		while True:
			for i in range(RUNTIME):
				for i in os.listdir('/sys/bus/w1/devices'):
					if i[:3] == '28-':
						self._ds18b20 = i
				if self._ds18b20 != '':
					print 'DS18B20 founded.\nSlave address:', self._ds18b20
					self._location = '/sys/bus/w1/devices/' + self._ds18b20
					break
				time.sleep(0.001)
			if self._ds18b20 != '':
				break
			else:
				print 'Timeout. No device. Check if Plus DS18B20 is pluged in.'
				print 'Press enter to try again, or Crrl + C to quit.'
				_tmp = raw_input()

	def get_temperature(self, unit=0):
		_location = self._location + '/w1_slave'
		while True:
			for i in range(RUNTIME):
				try:
					_tfile = open(_location)
					_text = _tfile.read()
					_tfile.close()
					_secondline = _text.split("\n")[1]
					if _secondline == '00 00 00 00 00 00 00 00 00 t=0':
						_flag = 0
					else:
						_flag = 1
						break
					time.sleep(0.001)
				except:
					_flag = 0
			if _flag == 1:
				break
			else:
				print 'Timeout. No device. Check if Plus DS18B20 is pluged in.'
				print 'Press enter to try again, or Crrl + C to quit.'
				_tmp = raw_input()

		_temperaturedata = _secondline.split(" ")[9]
		_temperature = float(_temperaturedata[2:])
		_temperature_c = _temperature / 1000
		if unit == self.C:
			return _temperature_c
		if unit == self.F:
			_temperature_f = _temperature_c * 9.0 / 5.0 + 32.0
			return _temperature_f
'''

class Speech_Recognition(_Basic_class):

	_class_name = 'Speech_Recognition'
	import SpeakPythonRecognizer

	def __init__(self, dictionary, name_calling=False, timeout=5.0, dictionary_update=False):
		self.name_calling = name_calling
		self.dictionary = dictionary
		self._result = 'None'
		if dictionary_update:
			self.update_dictionary()
		self.recog = SpeakPythonRecognizer.SpeakPythonRecognizer(self._get_result, self.dictionary)
		self.recog.setDebug(20)
		if self.name_calling:
			import threading
			self.timeout = timeout
			self._awake = False
			self.threading = threading

	def _is_timeout(self):
		self._awake = False
		self.debug('Time out, Sleep.')

	@property
	def result(self):
		return self._result

	def _get_result(self, out_str):
		if self.name_calling:
			self.debug('Name calling is true')
			if out_str == '__NAME__':
				self.debug('Called name is right')
				self._awake = True
				self.debug('Awake')
				try:
					self.t.cancel()
				except:
					pass
				finally:
					self.t = self.threading.Timer(self.timeout, self._is_timeout)
					self.t.start()
					self.debug('Count down begin')
					self._result = out_str
			elif self._awake:
				self._result = out_str
				try:
					self.t.cancel()
					self.debug('Count down stop')
				except:
					pass
				finally:
					self._awake = False
					self.debug('Sleep')
			else:
				self._result == ''
		else:
			self._result = out_str
			self.debug('Return %s' % out_str)


	def recognize(self):
		self.debug('Recognize Begin')
		self.recog.recognize()

	def update_dictionary(self):
		self.debug('Begin dictionary update')
		cmd = "sudo MakeSpeechProject.py %s %s.sps" % (self.dictionary, self.dictionary)
		self.run_command(cmd)
		self.debug('Update finished')
		return 0

	def end(self):
		self.debug('Recognize stop')
		self.recog.stop()
		self.recog.quit()

class TTS(_Basic_class):

	_class_name = 'TTS'
	ENGINE_LIST = ['festival', 'espeak', 'pico']

	def __init__(self, engine='pico'):
		self.engine = engine
		self._lang = "en-US"

	def _check_executable(self, executable):
		executable_path = find_executable(executable)
		found = executable_path is not None
		return found

	def say(self, words):
		self.debug('Engine [%s], say:\n [%s]' % (self.engine, words)) 
		if self.engine == 'festival':
			if self._check_executable('festival'):
				cmd = "echo '%s' | festival --tts & " % words
				self.run_command(cmd)
				self.debug('command: %s' %cmd)
			else:
				self.debug('Festival is busy. Pass')
		if self.engine == 'espeak':
			if self._check_executable('espeak'):
				cmd = 'espeak -a%d -s%d -g%d -p%d \"%s\" 2>/dev/null & ' % (self._amp, self._speed, self._gap, self._pitch, words)
				self.run_command(cmd)
				self.debug('command: %s' %cmd)
			else:
				self.debug('Festival is busy. Pass')
		if self.engine == 'pico':
			if self._check_executable('pico2wave') and self._check_executable('aplay'):
				cmd = 'pico2wave -l %s -w pico.wav "%s" && aplay pico.wav' % (self._lang, words)
				self.run_command(cmd)
				self.debug('command: %s' %cmd)
			else:
				self.debug('Festival is busy. Pass')

	def end(self):
		self.run_command("rm -f pico.wav")

	@property
	def lang(self):
		return self._lang
	
	@lang.setter
	def lang(self, value):
		self.lang = value

	@property
	def engine(self):
		return self._engine

	@engine.setter
	def engine(self, value):
		if value not in self.ENGINE_LIST:
			raise ValueError ("Engine should be one of \"{0}\", not \"{1}\".".format(self.ENGINE_LIST, engine))
		self._engine = value
		if self._engine == 'espeak':
			self._amp   = 100 
			self._speed = 175
			self._gap   = 5
			self._pitch = 50

	def espeak_params(self, amp=None, speed=None, gap=None, pitch=None):
		if self.engine != 'espeak':
			raise ValueError ('The TTS engine you choose is "{0}", please choose "espeak" to set espeak_params.\n \
				To choose espeak: TTS.engine = "espeak"').format(self.engine)
		else:
			if amp == None: 
				amp=self._amp
			if speed == None:
				speed=self._speed
			if gap == None:
				gap=self._gap
			if pitch == None:
				pitch=self._pitch

			if amp not in range(0, 200):
				raise ValueError('Amp should be in 0 to 200, not "{0}"').format(amp)
			if speed not in range(80, 260):
				raise ValueError('Amp should be in 80 to 260, not "{0}"').format(speed)
			if pitch not in range(0, 99):
				raise ValueError('Amp should be in 0 to 99, not "{0}"').format(pitch)	
			self._amp   = amp
			self._speed = speed
			self._gap   = gap
			self._pitch = pitch

