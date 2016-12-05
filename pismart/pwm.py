from basic import _Basic_class

class PWM(_Basic_class):
    PWM_ADDRESS         = 0x40

    _LED0_ON_L          = 0x06
    _LED0_ON_H          = 0x07
    _LED0_OFF_L         = 0x08
    _LED0_OFF_H         = 0x09

    def __init__(self, channel):
        if channel not in range(0, 16):
            raise ValueError("PWM channel \"{0}\" is not in (0, 15).".format(channel))
        self.channel = channel
        self.logger_setup()

    def set_PWM(self, on, off=0):
        self.bus.write_byte_data(self.PWM_ADDRESS, self._LED0_ON_L+4*self.channel, off & 0xFF)
        self.bus.write_byte_data(self.PWM_ADDRESS, self._LED0_ON_H+4*self.channel, off >> 8)
        self.bus.write_byte_data(self.PWM_ADDRESS, self._LED0_OFF_L+4*self.channel, on & 0xFF)
        self.bus.write_byte_data(self.PWM_ADDRESS, self._LED0_OFF_H+4*self.channel, on >> 8)
