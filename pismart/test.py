from amateur import PiSmart
import time

pismart = PiSmart()

def adc():
    print pismart.A0

def servo():
    while True:
        for i in range(0, 181, 1):
            pismart.Servo0 = i
            time.sleep(0.01)
            print i
        time.sleep(2)
        for i in range(180, -1, -1):
            pismart.Servo0 = i
            time.sleep(0.01)
            print i
        time.sleep(2)

def led():
    delay = 0.01
    while True:
        for i in range(0, 100, 1):
            pismart.Red_LED = i
            time.sleep(delay)
        time.sleep(1)
        for i in range(100, -1, -1):
            pismart.Red_LED = i
            time.sleep(delay)
        time.sleep(1)
        for i in range(0, 100, 1):
            pismart.Blue_LED = i
            time.sleep(delay)
        time.sleep(1)
        for i in range(100, -1, -1):
            pismart.Blue_LED = i
            time.sleep(delay)
        time.sleep(1)

def motor():
    pismart.MotorA_reversed = True
    pismart.MotorA = 100
    pismart.MotorB = 100
    time.sleep(1)
    pismart.MotorA = 50
    pismart.MotorB = 50
    time.sleep(1)
    pismart.MotorA = 0
    pismart.MotorB = 0
    time.sleep(1)
    pismart.MotorA = -50
    pismart.MotorB = -50
    time.sleep(1)
    pismart.MotorA = -100
    pismart.MotorB = -100
    time.sleep(1)
    pismart.MotorA = 0
    pismart.MotorB = 0

def switchs():
    print 'Set speaker volume to 100...',
    pismart.speaker_volume = 100
    print 'done'
    print 'Speaker volume now is', pismart.speaker_volume
    print 'Set capture volume to 100...',
    pismart.capture_volume = 100
    print 'done'
    print 'Capture volume now is', pismart.capture_volume
    print 'Set power type to DC...',
    pismart.power_type = 'DC'
    print 'done'
    print 'Power type now is', pismart.power_type
    print ''
    print 'Power voltage now is', pismart.power_voltage
    print 'Switch the servo on...',
    pismart.servo_switch(pismart.ON)
    print 'done'
    print 'Switch the PWM on...',
    pismart.pwm_switch(pismart.ON)
    print 'done'
    print 'Switch the motor on...',
    pismart.motor_switch(pismart.ON)
    print 'done'
    print 'Switch the speaker on...',
    pismart.speaker_switch(pismart.ON)
    print 'done'

    print 'Switch the servo off...',
    pismart.servo_switch(pismart.OFF)
    print 'done'
    print 'Switch the PWM off...',
    pismart.pwm_switch(pismart.OFF)
    print 'done'
    print 'Switch the motor off...',
    pismart.motor_switch(pismart.OFF)
    print 'done'
    print 'Switch the speaker off...',
    pismart.speaker_switch(pismart.OFF)
    print 'done'

def tts():
    print pismart.Say
    pismart.Say = "Yes, i am"

def volume_test():
    for i in range(100, -1, -10):
        print 'Set speaker volume to %s...' % i
        pismart.speaker_volume = i
        pismart.Say = 'This is %s percent volume' % i

if __name__ == '__main__':
    try:
        tts()
    except KeyboardInterrupt:
        pismart.end()