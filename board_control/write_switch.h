#include <Arduino.h>
#define WRITE_DEBUG         false   // DEBUG = true,print message
#define READ_DEBUG          false

/* The level to contral switch */
#define RPIPOWERON 			1
#define RPIPOWEROFF 		0
#define SERVOPOWERON 		1
#define SERVOPOWEROFF 		0
#define MOTORPOWERON 		1
#define MOTORPOWEROFF 		0
#define SPEAKERPOWERON 		0
#define SPEAKERPOWEROFF 	1
#define MICSWITCHON 		1
#define MICSWITCHOFF 		0
#define STATUSLEDON 		1
#define STATUSLEDOFF 		0

/* pins connection */
#define motorPowerSwitch     4
#define speakerPowerSwitch   5
#define rpiPowerSwitch       6
#define servoPowerSwitch     7
#define micSwitch            8
#define powerOffDetect       9
#define statusLed            10


/* contral switches */
extern void IO_init();
extern void servoSwitchCtrl(int onoff);
extern void motorSwitchCtrl(int onoff);
extern void speakerSwitchCtrl(int onoff);
extern void rpiSwitchCtrl(int onoff);
extern void micSwitchCtrl(int onoff);
extern void statusLedCtrl(int onoff);
