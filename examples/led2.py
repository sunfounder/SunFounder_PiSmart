from pismart.led import LED
import time

blue_leds = LED(LED.LED1)
red_leds  = LED(LED.LED2)

LED_MAX = 100 
LED_MIN = 10

def main():
    while True:
        for x in xrange(1,3):
            for x in xrange(LED_MIN, LED_MAX, 5):
                blue_leds.brightness = x
                time.sleep(0.003)
            for x in xrange(LED_MAX, LED_MIN, -5):
                blue_leds.brightness = x
                time.sleep(0.005)
        blue_leds.off()

        for x in xrange(1,3):
            for x in xrange(LED_MIN, LED_MAX, 5):
                red_leds.brightness = x
                time.sleep(0.003)
            for x in xrange(LED_MAX, LED_MIN, -5):
                red_leds.brightness = x
                time.sleep(0.005)
        red_leds.off()

def destroy():
    red_leds.off()
    blue_leds.off()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

