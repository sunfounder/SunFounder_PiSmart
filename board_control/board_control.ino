#include <Wire.h>
#include <Enerlib.h>      // energy library
#include <MsTimer2.h>
#include "led.h"
#include "write_switch.h"


#define DEBUG             false   // DEBUG = true,print message
#define I2C_DEBUG         false
#define BATTERY_DEBUG     false
#define WRITE_DEBUG       false   // DEBUG = true,print message
#define READ_DEBUG        false

#define SLAVE_ADDRESS     0x10

#define READ              1 			// READ  get value 
#define WRITE             2 			// WRITE contral switch

int powerType = 1;
float alarm_gate[3] = {0, 7.4, 11.1};
bool isLowPower = false;

#define CHANNEL0          0x10
#define CHANNEL1          0x12
#define CHANNEL2          0x14
#define CHANNEL3          0x16
#define CHANNEL4          0x18
#define POWERVOLTAGE      0x1a
#define ISPOWEROFF 	      0x1C

/* instructions that arduino will get */
#define SERVO_POWER_OFF   0x20
#define SERVO_POWER_ON    0x21
#define SPEAKER_POWER_OFF 0x22
#define SPEAKER_POWER_ON  0x23
#define MOTOR_POWER_OFF   0x24
#define MOTOR_POWER_ON    0x25
#define SET_POWER_DC      0X26	// powerType = 0, DC power
#define SET_POWER_2S      0X27	// powerType = 1, Li-po battery 2s
#define SET_POWER_3S      0X28	// powerType = 2, Li-po battery 3s

#define BATTERYCHECKDELAY   60000	// every 60s, the timer_ISR will tell system to check battery
#define SLEEPDELAY          15000
#define LONGPRESS           2000

int number; 				// recieve the instructions from i2c
unsigned int buf = 0; 		// analog value, be going to send on i2c

/* power switch  */
unsigned long pressTime;
unsigned long releaseTime;
int isReleased = 1;

int swPin= 2;	// swPin connect

/* registration of the statues */
bool checkBatterySignal = true;
int sleepSignal      = 0;   // sleepSignal =2, sleep; sleepSignal =1, awake
int statusLedOutput = 1; 	// 1 = on； 0 = off
int count            = 0;	// statusLed blink timer

int lastPowerStatus  = 1;   // when raspberry off, powerOffDetect = 1

int analogList[2] = {0,0};
int ANALOG_CHANNEL[6] = {0, 1, 2, 3, 6, 7};  // analog channel of arduino,A4,A5 is used as i2c;
bool isReceived = 0; 		// finished receving data, flag = 1
bool isSent = false;

Energy energy;


int read_or_write = 0;   // read analog value or contral switch
int channel = 0;

void setup() {

  if (DEBUG) {Serial.begin(9600);}

  //======== Pins Setup ========
  IO_init();
  pinMode(swPin, 		INPUT_PULLUP);
  attachInterrupt(0, wake_ISR, CHANGE);

  if (DEBUG){Serial.println("Ready! Press button to wake.");}

  energy.PowerDown();
}

void loop() {
	/* finished receiving data */
	if (isReceived == 1) {
		read_or_write = number >> 4;
		channel = number & 0x0F;
		if (I2C_DEBUG){
			Serial.println("\n====== Finished recieve=======\n");
			Serial.print("channel = 0x");Serial.println(channel, HEX);
		}
		switch (read_or_write) {
			case READ:
				if(channel < 0xC)
					buf = readAnalog(channel);
				else
					buf = sleepSignal;
				if (I2C_DEBUG) {
					Serial.print("buf = ");
					Serial.print("0x"); Serial.println(buf, HEX);
				}
				break;
			case WRITE:
				writeSwitch(number);
				break;
		}
		isReceived = 0;
	}

	/* sleepSignal == 1 , wake arduino up and power raspberry on */
	if (sleepSignal == 1) {
		if (DEBUG) {Serial.println("Waked up");}
		rpiSwitchCtrl(RPIPOWERON);
		micSwitchCtrl(MICSWITCHON);
		statusLedCtrl(1);
		if (DEBUG) {Serial.println("RPiPowerSwitch is ON");}
		delay(500);
		ledBreathPowerOn(); 		// Breath effect
		sleepSignal = 0 ; 			// Clear signal
		if (DEBUG) {
			Serial.println("Led breath power on finished. Begin i2c slave");
			Serial.println("\n");
		}
		//MsTimer2::set(BATTERYCHECKDELAY, batteryCheckISR); // 60s period
		//MsTimer2::start();
		/* Set arduino as slave, Raspberry Pi as master */
		Wire.end();
		Wire.begin(SLAVE_ADDRESS);
		Wire.onReceive(receiveData);
		Wire.onRequest(sendData);
	}

	/* sleepSignal == 2 , go to sleep */
	if (sleepSignal == 2) {
		if(isSent && channel == 0xC && buf == sleepSignal){
			sleepSignal = 0 ;       // signal clear
			doSleep();
		}
	}

	if (checkBatterySignal){
		checkBattery();
		checkBatterySignal = false; 
	}

	if (isLowPower){
		count ++;
		if(count == 30000){
			statusLedOutput = !statusLedOutput;
			statusLedCtrl(statusLedOutput);
			count = 0;
			if(BATTERY_DEBUG){Serial.println("  Battery  power is low");}           
		}
	}
}


void writeSwitch(int number) {
	
	if (WRITE_DEBUG) {
		Serial.println("========= Write switch begin! ==========");
		Serial.print("  Switch channel :");
		Serial.println(number & 0x0F);
	}

	switch (number) {
		case SERVO_POWER_OFF:
			if (WRITE_DEBUG) {
				Serial.println("  Servo POWEROFF");
			}
			digitalWrite(servoPowerSwitch, SERVOPOWEROFF);
			break;
		case SERVO_POWER_ON:
			if (WRITE_DEBUG) {
				Serial.println("  Servo POWERON");
			}
			digitalWrite(servoPowerSwitch, SERVOPOWERON);
			break;
		case SPEAKER_POWER_OFF:
			if (WRITE_DEBUG) {
				Serial.println("  Speaker POWEROFF");
			}
			digitalWrite(speakerPowerSwitch, SPEAKERPOWEROFF);
			break;
		case SPEAKER_POWER_ON:
			if (WRITE_DEBUG) {
				Serial.println("  Speaker POWERON");
			}
			digitalWrite(speakerPowerSwitch, SPEAKERPOWERON);
			break;
		case MOTOR_POWER_OFF:
			if (WRITE_DEBUG) {
				Serial.println("  Motor POWEROFF");
			}
			digitalWrite(motorPowerSwitch, MOTORPOWEROFF);
			break;
		case MOTOR_POWER_ON:
			if (WRITE_DEBUG) {
				Serial.println("  Motor POWERON");
			}
			digitalWrite(motorPowerSwitch, MOTORPOWERON);
			break;
		case SET_POWER_DC:
			checkBatterySignal = true;
			if (WRITE_DEBUG){
				Serial.println("  Use DC power");
			}
			powerType = 0;
			break;  
		case SET_POWER_2S:
			checkBatterySignal = true;
			if (WRITE_DEBUG){
				Serial.println("  Use 2S battery");
			}
			powerType = 1;
			break;
		case SET_POWER_3S:
			checkBatterySignal = true;
			if (WRITE_DEBUG){
				Serial.println("  Use 3S battery");
			}
			powerType = 2;
			break;    	
	}
}

/* Read analog value , then put the value to buf */
int readAnalog(int channel) {
	unsigned int buf = 0; 		// analog value, be going to send on i2c
	int analogValue = 0;
	// 0x1n read channel x, the second number of 'number' means the channel to read
	if (READ_DEBUG) {
		Serial.println(" ");
		Serial.println("========== Read analog begin! ==========");
		Serial.print("  recieve number: ");Serial.println(number,HEX);
		Serial.print("  Reading channel: ");Serial.println(channel / 2);
	}

	//if((number % 2) == 0){     // value_H read pin value, next value_L don't need read again
		analogValue = analogRead(ANALOG_CHANNEL[channel / 2]);
		analogList[0] = (analogValue >> 8);		// analogList[0] high 8 bit
		analogList[1] = (analogValue & 0x00FF);	// analogList[1] low  8 bit
	//}
	buf = analogList[channel % 2];					// choose to send analogList[0] or analogList[1]
	if (READ_DEBUG) {
		if (channel % 2 == 0) {
			Serial.print("  Channel value: ");Serial.println(analogValue);
			Serial.print("    HighByte: ");Serial.println(buf,HEX);
		}
		if (channel % 2 == 1) {
			Serial.print("    LowByte: ");Serial.println(buf,HEX);
			Serial.println("========= Read analog finished! ========");
			Serial.println(" ");
		}
	}
	return buf;
}


/* This function will call if interrupted
   short press: sleepSignal = 1(is sleep) or 0(is awake)
   long press:  sleepSignal = 2(is awake)
*/
void wake_ISR() {
	isReleased = digitalRead(swPin); // 1 = released; 0 = pressed
	if (DEBUG) {
		Serial.println("========= Button ISR detected! =========");
	}
	if (isReleased == 1) {           // when release the button, change the signal
		releaseTime = millis();
		if (DEBUG) {Serial.println("  Button releaseed");}
		if ((releaseTime - pressTime) > LONGPRESS) { // long pressed
			sleepSignal = 2;
			if (DEBUG) {Serial.println("    Type: long press");}
		}
		else {                                     // short pressed
			if (energy.WasSleeping()) {
				sleepSignal = 1;
			}
			if (DEBUG) {Serial.println("    Type: short press");}
		}
		if (DEBUG) {
			Serial.print("  pressTime ="); Serial.println(pressTime);
			Serial.print("  releaseTime ="); Serial.println(releaseTime);
			Serial.print("  sleepSignal is "); Serial.println(sleepSignal);
		}
	}
	else {   // when pressed the button, mark time
		pressTime = millis();
		if (DEBUG) {Serial.println("  Button pressed");}
	}
}

void batteryCheckISR() {
	checkBatterySignal = true;
	if(BATTERY_DEBUG){Serial.println("Check battery");}
}

void checkBattery() {
	/*
	function: read and caculate system voltage,
		if votage < 6V, system will sleep;
		if votage < powerType gate , system will flash led
	 */
	float A7_value, A7_voltage, batteryVoltage;

	A7_value = analogRead(A7);
	A7_voltage = A7_value / 1024 * 5;
	batteryVoltage = A7_voltage * 14.7 / 4.7;
	if(BATTERY_DEBUG){
		Serial.print("  System power is ");Serial.print(batteryVoltage);Serial.println("V");
	} 

	// system need at least 6V voltage to work, if less then 6v, go to sleep
	if(batteryVoltage < 6){		
		if(BATTERY_DEBUG){Serial.println("  System power is less then 6V, and go to sleep");}
		for(int i=0; i<26; i++){
			statusLedCtrl(STATUSLEDOFF);
			delay(100);
			statusLedCtrl(STATUSLEDON);
			delay(100);  
		}
		doSleep();
	}
	// raspi will tell arduino powerType, every power-type has different alarm gate
	else if(batteryVoltage < alarm_gate[powerType]){	
		isLowPower = true;
	}
	else
		isLowPower = false;
}

/* when there has data on i2c , recieveData() will run*/
void receiveData(int byteCount) {
	if (I2C_DEBUG) {
		Serial.println("============ Data received! ============");
	}

	while (Wire.available()) {
		number = Wire.read();
	}
	isReceived = 1;
	if (I2C_DEBUG) {
		Serial.print("  Received number = 0x");
		Serial.println(number, HEX);
	}
}

void sendData() {
	if (I2C_DEBUG) {
		Serial.println("============== Data Sent! ==============");
		Serial.print("  Sent value: "); Serial.println(buf);
		Serial.println("");
	}
	delay(1);
	Wire.write(buf);
	isSent = true;
}

/* arduino sleep , and turn off other device */
void doSleep() {
  double poweroffDelayBegin;
  double poweroffDelayEnd;
	if (DEBUG) {
		Serial.println("============= Sleep begin! =============");
	}
	servoSwitchCtrl(SERVOPOWEROFF);
	motorSwitchCtrl(MOTORPOWEROFF);
	speakerSwitchCtrl(SPEAKERPOWEROFF);
	micSwitchCtrl(MICSWITCHOFF);
	statusLedCtrl(STATUSLEDON);

	/*delay 'SLEEPDELAY' to turn off rpi , because that rpi shut down need sometime */
	if (DEBUG) {                   // if debug , need more time
		Serial.println(" Waiting for Raspberry Pi shut down");
	}
	do{
		powerOffLedBreathUp();        // led breath effect
		powerOffLedBreathDown();        // led breath effect
		if (isRaised()) 
			poweroffDelayBegin = millis();
		if (digitalRead(powerOffDetect))
			poweroffDelayEnd = millis();
	} while ((poweroffDelayEnd - poweroffDelayBegin) > 4000000);
	if (DEBUG) {
		Serial.print("  Raspberry Pi is off");
	}
	rpiSwitchCtrl(RPIPOWEROFF);
	if (DEBUG) {
		Serial.println("  Raspberry Pi Power is OFF ");
		Serial.println("  Go to sleep.");
	}
	energy.PowerDown();           // Arduino go to sleep
}

bool isRaised(){
	bool currentPowerStatus;
	bool raised = false;
	currentPowerStatus = digitalRead(powerOffDetect);
	if (lastPowerStatus == 0 && currentPowerStatus == 1){
		raised = true;
	}
	lastPowerStatus = currentPowerStatus;
	return raised;
}
