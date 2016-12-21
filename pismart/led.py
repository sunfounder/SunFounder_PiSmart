from basic import _Basic_class
from pwm import PWM

class LED(PWM):

    RED         = 9
    BLUE        = 8
    BRIGHT      = 75
    RUNING      = 30
    DIMING      = 5
    OFF         = 0
    
    LED_PIN = {'red':9, 'blue':8}
    LED_COLOR = {9:'LED.RED', 8:'LED.BLUE'}

    BRIGHT_X = 100          #how long it will be bright 
    SLEEP_TIME  = 0.02

    _class_name = 'LED'

    def __init__(self, channel=None):
        self.logger_setup()
        self.channel = channel
        self.brightness = 0

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        if isinstance(channel, str):
            if channel.lower() in self.LED_PIN:
                channel = self.LED_PIN.get(channel.lower())
        elif channel not in range(10):
            raise ValueError("LED channel \"{0}\" is not in (0, 9).".format(channel))
        elif channel not in (8, 9):
            self.warning('Led channel "%s" is not the ring. The ring should be "RED"(9) or "BLUE"(8), '%channel)
        self._channel = channel
        self._debug("Channel set to [%s]" % self._channel)

    def _get_pwm_from_brightness(self, brightness):
        pwm_value = self._map(brightness, 0, 100, 0, 4095)
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
        self._debug('Set LED [%s] to [%s].' % (self.LED_COLOR[self.channel], self._brightness))

    def write(self, value):
        self.brightness = value

    def off(self):
        pwm_value = self._get_pwm_from_brightness(self.OFF)
        self.set_PWM(self.OFF)
        self._debug('Set LED [%d] OFF.' % self.channel)