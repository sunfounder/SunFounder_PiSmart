#include <Arduino.h>
#define LED_DEBUG         false   // DEBUG = true,print message

/* use to contral the led ring */
#define  RED 				9
#define  BLUE 				8
#define  BRIGHT 			60
#define  RUNING 			30
#define  DIMING 			10
#define  OFF 				0
#define  BREATH_DELAY 		20

extern void breath(int start_value, int end_value, int led);
extern void led_breath_power_on();
extern void led_breath_power_off();


