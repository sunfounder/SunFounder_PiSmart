import smbus
import logging

class _Basic_class(object):

    _class_name = '_Basic_class'
    _DEBUG = 0
    DEBUG_LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL,
              }
    DEBUG_NAMES = ['critical', 'error', 'warning', 'info', 'debug']

    bus = smbus.SMBus(1)

    def __init__(self):
        pass
        
    def logger_setup(self):
        self.logger = logging.getLogger(self._class_name)
        self.ch = logging.StreamHandler()
        self.formatter = logging.Formatter("%(asctime)s  pismart  class %s  %(levelname)s  %(message)s" % self._class_name)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        self._debug    = self.logger.debug
        self._info     = self.logger.info
        self._warning  = self.logger.warning
        self._error    = self.logger.error
        self._critical = self.logger.critical

    @property
    def DEBUG(self):
        return self._DEBUG
    
    @DEBUG.setter
    def DEBUG(self, debug):
        if debug in range(5):
            self._DEBUG = self.DEBUG_NAMES[debug]
        elif debug in self.DEBUG_NAMES:
            self._DEBUG = debug
        else:
            raise ValueError('Debug value must be 0(critical), 1(error), 2(warning), 3(info) or 4(debug), not \"{0}\".'.format(debug))  
        self.logger.setLevel(self.DEBUG_LEVELS[self._DEBUG])
        self.ch.setLevel(self.DEBUG_LEVELS[self._DEBUG])
        self._debug('Set debug %s' % debug)

    def run_command(self, cmd):
        self._debug('Run command: "%s"' % cmd)
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, shell=True, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            return output

    @staticmethod
    def _map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
