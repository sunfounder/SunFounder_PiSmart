#include "write_switch.h"

int analogList[2] = {0,0};
int ANALOG_CHANNEL[6] = {0, 1, 2, 3, 6, 7};  // analog channel of arduino,A4,A5 is used as i2c;

void IO_init(){
  //======== Pins Setup ========
  pinMode(MotorPowerSwitch, 	OUTPUT);
  pinMode(ServoPowerSwitch, 	OUTPUT);
  pinMode(RPiPowerSwitch, 		OUTPUT);
  pinMode(SpeakerPowerSwitch, 	OUTPUT);
  pinMode(StatusLed, 			OUTPUT);
  pinMode(PowerOffDetect, 		OUTPUT);
  pinMode(MicSwitch, 			OUTPUT);

  digitalWrite(ServoPowerSwitch, 	SERVOPOWEROFF);
  digitalWrite(MotorPowerSwitch, 	MOTORPOWEROFF);
  digitalWrite(SpeakerPowerSwitch, 	SPEAKERPOWEROFF);
  digitalWrite(MicSwitch, 			MICSWITCHOFF);
  digitalWrite(RPiPowerSwitch, 		RPIPOWEROFF);
  digitalWrite(PowerOffDetect, 		RPIPOWERON);
  digitalWrite(StatusLed, 			STATUSLEDON);

}

/* contral switches */
void servo_switch_ctrl(int onoff){
	digitalWrite(ServoPowerSwitch, onoff);
}
void motor_switch_ctrl(int onoff){
	digitalWrite(MotorPowerSwitch, onoff);
}
void speaker_switch_ctrl(int onoff){
	digitalWrite(SpeakerPowerSwitch, onoff);
}
void rpi_switch_ctrl(int onoff){
	digitalWrite(RPiPowerSwitch, onoff);
}
void mic_switch_ctrl(int onoff){
	digitalWrite(MicSwitch, onoff);
}
void status_led_ctrl(int onoff){
	digitalWrite(StatusLed, onoff);
}
void rpi_shutdown_ctrl(int onoff){
	digitalWrite(PowerOffDetect, onoff);
}
