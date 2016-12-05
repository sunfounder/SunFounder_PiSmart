from basic import _Basic_class

class STT(_Basic_class):
    _class_name = 'STT'
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
        self.logger_setup()

    def _is_timeout(self):
        self._awake = False
        self._debug('Time out, Sleep.')

    @property
    def result(self):
        return self._result

    def _get_result(self, out_str):
        if self.name_calling:
            self._debug('Name calling is true')
            if out_str == '__NAME__':
                self._debug('Called name is right')
                self._awake = True
                self._debug('Awake')
                try:
                    self.t.cancel()
                except:
                    pass
                finally:
                    self.t = self.threading.Timer(self.timeout, self._is_timeout)
                    self.t.start()
                    self._debug('Count down begin')
                    self._result = out_str
            elif self._awake:
                self._result = out_str
                try:
                    self.t.cancel()
                    self._debug('Count down stop')
                except:
                    pass
                finally:
                    self._awake = False
                    self._debug('Sleep')
            else:
                self._result == ''
        else:
            self._result = out_str
            self._debug('Return %s' % out_str)


    def recognize(self):
        self._debug('Recognize Begin')
        self.recog.recognize()

    def update_dictionary(self):
        self._debug('Begin dictionary update')
        cmd = "sudo MakeSpeechProject.py %s %s.sps" % (self.dictionary, self.dictionary)
        self.run_command(cmd)
        self._debug('Update finished')
        return 0

    def end(self):
        self._debug('Recognize stop')
        self.recog.stop()
        self.recog.quit()
