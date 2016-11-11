#include "write_switch.h"

//int analogList[2] = {0,0};
//int ANALOG_CHANNEL[6] = {0, 1, 2, 3, 6, 7};  // analog channel of arduino,A4,A5 is used as i2c;

void IO_init(){
  //======== Pins Setup =======rSwitch,  OUTPUT);
  pinMode(servoPowerSwitch, OUTPUT);
  pinMode(motorPowerSwitch, OUTPUT);
  pinMode(rpiPowerSwitch, 		OUTPUT);
  pinMode(speakerPowerSwitch, 	OUTPUT);
  pinMode(statusLed, 			OUTPUT);
  pinMode(powerOffDetect, 		INPUT);
  pinMode(micSwitch, 			OUTPUT);

  digitalWrite(servoPowerSwitch, 	SERVOPOWEROFF);
  digitalWrite(motorPowerSwitch, 	MOTORPOWEROFF);
  digitalWrite(speakerPowerSwitch, 	SPEAKERPOWEROFF);
  digitalWrite(micSwitch, 			MICSWITCHOFF);
  digitalWrite(rpiPowerSwitch, 		RPIPOWEROFF);
  digitalWrite(powerOffDetect, 		RPIPOWERON);
  digitalWrite(statusLed, 			STATUSLEDON);

}

/* contral switches */
void servoSwitchCtrl(int onoff){
	digitalWrite(servoPowerSwitch, onoff);
}
void motorSwitchCtrl(int onoff){
	digitalWrite(motorPowerSwitch, onoff);
}
void speakerSwitchCtrl(int onoff){
	digitalWrite(speakerPowerSwitch, onoff);
}
void rpiSwitchCtrl(int onoff){
	digitalWrite(rpiPowerSwitch, onoff);
}
void micSwitchCtrl(int onoff){
	digitalWrite(micSwitch, onoff);
}
void statusLedCtrl(int onoff){
	digitalWrite(statusLed, onoff);
}
