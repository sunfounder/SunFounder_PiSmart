from pismart.amateur import PiSmart
from time import sleep

def setup():
    global sample
    sample = PiSmart()
    # If one of the motor is reversed, change its False to True
    sample.MotorA_reversed = False
    sample.MotorB_reversed = False

def end():
    sample.end()

def loop():
    # Erase pass below and add your code here
    pass

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        end()

