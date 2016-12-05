from basic import _Basic_class
from pwm import PWM

class Servo(PWM):
    _MIN_PULSE_WIDTH    = 544
    _MAX_PULSE_WIDTH    = 2400
    _FREQUENCY          = 60

    _class_name = 'Servo'

    def __init__(self, channel, offset=0):
        if channel not in range(0, 8):
            raise ValueError("Servo channel \"{0}\" is not in (0, 7).".format(channel))
        self.channel = channel
        self._offset = offset
        self.logger_setup()

    def _angle_to_analog(self, angle):
        pulse_wide   = _map(angle, 0, 180, self._MIN_PULSE_WIDTH, self._MAX_PULSE_WIDTH)
        analog_value = int(float(pulse_wide) / 1000000 * self._FREQUENCY * 4096)
        return analog_value
        
    def write(self, angle):
        if angle<0 or angle>180:
            raise ValueError("Servo \"{0}\" turn angle \"{1}\" is not in (0, 180).".format(self.channel, angle))        
        value = self._angle_to_analog(angle)
        value += self._offset
        self.set_PWM(value)
        self._debug('Servo turn. channel: [%d] to angle: [%d]' % (self.channel, angle))

    def turn(self, angle):
        self.write(angle)

    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self, value):
        self._offset = value
