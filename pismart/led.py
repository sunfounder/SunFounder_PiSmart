from basic import _Basic_class
from pwm import PWM

class LED(PWM):

    RED         = 9
    BLUE        = 8
    BRIGHT      = 75
    RUNING      = 30
    DIMING      = 5
    OFF         = 0
    
    LED_COLOR = {'red':9, 'blue':8}

    BRIGHT_X = 100          #how long it will be bright 
    SLEEP_TIME  = 0.02

    _class_name = 'LED'

    def __init__(self, channel):
        if isinstance(channel, str):
            if channel.lower() in self.LED_COLOR:
                channel = self.LED_COLOR.get(channel.lower())
        if channel not in (8, 9):
            raise ValueError ('Led channel should be "RED"(9) or "BLUE"(8), not \"{0}\".'.format(channel))
        self.channel = channel
        self.logger_setup()
        self._debug('Init LED channel [%d] complate. (8 = BLUE, 9 = RED)' % self.channel)

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
        self._debug('Set LED [%d] to [%d].' % (self.channel, self._brightness))

    def off(self):
        pwm_value = self._get_pwm_from_brightness(self.OFF)
        self.set_PWM(self.OFF)
        self._debug('Set LED [%d] OFF.' % self.channel)