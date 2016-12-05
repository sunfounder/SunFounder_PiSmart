from basic import _Basic_class
from pwm import PWM

class Motor(PWM):
    MOTOR_CHANNEL = {'motora':0, 'motorb':1, 10:5, 11:6}

    OFF = 0

    _class_name = 'Motor'

    def __init__(self, channel, forward=0):
        if isinstance(channel, str):
            if channel.lower() in self.MOTOR_CHANNEL:
                channel = self.MOTOR_CHANNEL.get(channel.lower())
        if channel not in (0, 1):
            raise ValueError ('Motor channel should be "MotorA"(0) or "MotorB"(1), not "{0}".'.format(channel))
        self.channel = channel + 10
        self.logger_setup()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTOR_CHANNEL[self.channel], GPIO.OUT)
        if forward not in (0, 1):
            raise ValueError ("Forward direction should be 0 or 1, not \"{0}\".".format(forward))
        self._forward_direction = forward
        self._backward_direction = (forward + 1) & 1
        self._debug('Init motor channel [%d] complate. (10 = MOTOR_A, 11 = MOTOR_B)' % self.channel)

    def _speed_to_analog(self, speed):
        pwm_value = _map(speed, 0, 100, 0, 4095)
        self._debug('  speed: %d,  ->   pwm_value: %d' % (speed, pwm_value))
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
        self._debug('Motor forward direction channel[%d], pwm channel [%d]' % (self.MOTOR_CHANNEL[self.channel], self.channel))

    def backward(self, speed=50):
        if speed not in xrange(0, 101):
            raise ValueError ("Motor backward speed should be in (0, 100) not \"{0}\".".format(speed))
        analog_value = self._speed_to_analog(speed)
        self.set_PWM(analog_value)
        GPIO.output(self.MOTOR_CHANNEL[self.channel], self._backward_direction)
        self._debug('Motor backward, direction channel [%d], pwm channel [%d]' % (self.MOTOR_CHANNEL[self.channel], self.channel))

    def stop(self):
        self.set_PWM(self.OFF)
        GPIO.output(self.MOTOR_CHANNEL[self.channel], 0)
        self._debug('Motor stop, direction channel [%d], pwm channel [%d]' % (self.MOTOR_CHANNEL[self.channel], self.channel))
