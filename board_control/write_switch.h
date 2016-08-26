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
#define MotorPowerSwitch     4
#define SpeakerPowerSwitch   5
#define RPiPowerSwitch       6
#define ServoPowerSwitch     7
#define MicSwitch            8
#define PowerOffDetect       9
#define StatusLed            10


/* contral switches */
extern void IO_init();
extern void servo_switch_ctrl(int onoff);
extern void motor_switch_ctrl(int onoff);
extern void speaker_switch_ctrl(int onoff);
extern void rpi_switch_ctrl(int onoff);
extern void mic_switch_ctrl(int onoff);
extern void status_led_ctrl(int onoff);
extern void rpi_shutdown_ctrl(int onoff);
