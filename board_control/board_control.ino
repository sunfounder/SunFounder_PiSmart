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

int power_type = 1;
float alarm_gate[3] = {0, 7.4, 11.1};
bool low_power = false;

#define CHANNEL0          0x10
#define CHANNEL1          0x11
#define CHANNEL2          0x12
#define CHANNEL3          0x13
#define CHANNEL4          0x14
#define POWERVOLTAGE      0x15

/* instructions that arduino will get */
#define SERVO_POWER_OFF   0x20
#define SERVO_POWER_ON    0x21
#define SPEAKER_POWER_OFF 0x22
#define SPEAKER_POWER_ON  0x23
#define MOTOR_POWER_OFF   0x24
#define MOTOR_POWER_ON    0x25
#define SET_POWER_DC      0X26	// power_type = 0, DC power
#define SET_POWER_2S      0X27	// power_type = 1, Li-po battery 2s
#define SET_POWER_3S      0X28	// power_type = 2, Li-po battery 3s

#define BATTERYCHECKDELAY   60000	// every 60s, the timer_ISR will tell system to check battery
#define SLEEPDELAY          15000
#define LONGPRESS           2000

int number; 				// recieve the instructions from i2c
int number_flag = 0; 		// finished receving data, flag = 1
unsigned int a = 0; 		// analog value, be going to send on i2c

/* power switch  */
unsigned long press_time;
unsigned long release_time;
int release_flag = 1;

int swPin= 2;	// swPin connect

/* registration of the statues */
bool Check_batterySignal = true;
int SleepSignal      = 0;   // SleepSignal =2, sleep; SleepSignal =1, awake
int statusLed_output = 1; 	// 1 = on； 0 = off
int count            = 0;	// statusLed blink timer

int analogList[2] = {0,0};
int ANALOG_CHANNEL[6] = {0, 1, 2, 3, 6, 7};  // analog channel of arduino,A4,A5 is used as i2c;

Energy energy;

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
	int read_or_write = 0;   // read analog value or contral switch

	/* finished receiving data */
	if (number_flag == 1) {
		read_or_write = number >> 4;
		if (I2C_DEBUG){
			Serial.println("\n====== Finished recieve=======\n");
		}
		switch (read_or_write) {
			case READ:
				a = read_analog(number);
				number_flag = 0;
				if (I2C_DEBUG) {
					Serial.print("a = ");
					Serial.print("0x"); Serial.println(a, HEX);
				}
				break;
			case WRITE:
				write_switch(number);
				number_flag = 0;
				break;
		}
	}

	/* SleepSignal == 1 , wake arduino up and power raspberry on */
	if (SleepSignal == 1) {
		if (DEBUG) {Serial.println("Waked up");}
		rpi_switch_ctrl(RPIPOWERON);
		mic_switch_ctrl(MICSWITCHON);
		rpi_shutdown_ctrl(RPIPOWERON);
		status_led_ctrl(1);
		if (DEBUG) {Serial.println("RPiPowerSwitch is ON");}
		delay(500);
		led_breath_power_on(); 		// Breath effect
		SleepSignal = 0 ; 			// Clear signal
		if (DEBUG) {
			Serial.println("Led breath power on finished. Begin i2c slave");
			Serial.println("\n");
		}
		MsTimer2::set(BATTERYCHECKDELAY, battery_check_ISR); // 60s period
		MsTimer2::start();
		/* Set arduino as slave, Raspberry Pi as master */
		Wire.end();
		Wire.begin(SLAVE_ADDRESS);
		Wire.onReceive(receive_data);
		Wire.onRequest(send_data);
	}

	/* SleepSignal == 2 , go to sleep */
	if (SleepSignal == 2) {
		if (DEBUG) {
			delay(2000);
		}
		delay(1000);
		SleepSignal = 0 ;       // signal clear
		rpi_shutdown_ctrl(RPIPOWEROFF);
		mic_switch_ctrl(MICSWITCHOFF);
		status_led_ctrl(1);
		do_sleep();
	}

	if (Check_batterySignal){
		check_battery();
		Check_batterySignal = false; 
	}

	if (low_power){
		count ++;
		if(count == 30000){
			statusLed_output = !statusLed_output;
			status_led_ctrl(statusLed_output);
			count = 0;
			if(BATTERY_DEBUG){Serial.println("  Battery  power is low");}           
		}
	}
}


void write_switch(int number) {
	
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
			digitalWrite(ServoPowerSwitch, SERVOPOWEROFF);
			break;
		case SERVO_POWER_ON:
			if (WRITE_DEBUG) {
				Serial.println("  Servo POWERON");
			}
			digitalWrite(ServoPowerSwitch, SERVOPOWERON);
			break;
		case SPEAKER_POWER_OFF:
			if (WRITE_DEBUG) {
				Serial.println("  Speaker POWEROFF");
			}
			digitalWrite(SpeakerPowerSwitch, SPEAKERPOWEROFF);
			break;
		case SPEAKER_POWER_ON:
			if (WRITE_DEBUG) {
				Serial.println("  Speaker POWERON");
			}
			digitalWrite(SpeakerPowerSwitch, SPEAKERPOWERON);
			break;
		case MOTOR_POWER_OFF:
			if (WRITE_DEBUG) {
				Serial.println("  Motor POWEROFF");
			}
			digitalWrite(MotorPowerSwitch, MOTORPOWEROFF);
			break;
		case MOTOR_POWER_ON:
			if (WRITE_DEBUG) {
				Serial.println("  Motor POWERON");
			}
			digitalWrite(MotorPowerSwitch, MOTORPOWERON);
			break;
		case SET_POWER_DC:
			Check_batterySignal = true;
			if (WRITE_DEBUG){
				Serial.println("  Use DC power");
			}
			power_type = 0;
			break;  
		case SET_POWER_2S:
			Check_batterySignal = true;
			if (WRITE_DEBUG){
				Serial.println("  Use 2S battery");
			}
			power_type = 1;
			break;
		case SET_POWER_3S:
			Check_batterySignal = true;
			if (WRITE_DEBUG){
				Serial.println("  Use 3S battery");
			}
			power_type = 2;
			break;    	
	}
}

/* Read analog value , then put the value to a */
int read_analog(int number) {
	int channel;
	unsigned int a = 0; 		// analog value, be going to send on i2c
	int analogValue = 0;
	channel = number & 0x0F;
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
	a = analogList[channel % 2];					// choose to send analogList[0] or analogList[1]
	if (READ_DEBUG) {
		if (channel % 2 == 0) {
			Serial.print("  Channel value: ");Serial.println(analogValue);
			Serial.print("    HighByte: ");Serial.println(a,HEX);
		}
		if (channel % 2 == 1) {
			Serial.print("    LowByte: ");Serial.println(a,HEX);
			Serial.println("========= Read analog finished! ========");
			Serial.println(" ");
		}
	}
	return a;
}

/* This function will call if interrupted
   short press: SleepSignal = 1(is sleep) or 0(is awake)
   long press:  SleepSignal = 2(is awake)
*/
void wake_ISR() {
	release_flag = digitalRead(swPin); // 1 = released; 0 = pressed
	if (DEBUG) {
		Serial.println("========= Button ISR detected! =========");
	}
	if (release_flag == 1) {           // when release the button, change the signal
		release_time = millis();
		if (DEBUG) {Serial.println("  Button releaseed");}
		if ((release_time - press_time) > LONGPRESS) { // long pressed
			SleepSignal = 2;
			if (DEBUG) {Serial.println("    Type: long press");}
		}
		else {                                     // short pressed
			if (energy.WasSleeping()) {
				SleepSignal = 1;
			}
			if (DEBUG) {Serial.println("    Type: short press");}
		}
		if (DEBUG) {
			Serial.print("  press_time ="); Serial.println(press_time);
			Serial.print("  release_time ="); Serial.println(release_time);
			Serial.print("  SleepSignal is "); Serial.println(SleepSignal);
		}
	}
	else {   // when pressed the button, mark time
		press_time = millis();
		if (DEBUG) {Serial.println("  Button pressed");}
	}
}

void battery_check_ISR() {
	Check_batterySignal = true;
	if(BATTERY_DEBUG){Serial.println("Check battery");}
}

void check_battery() {
	/*
	function: read and caculate system voltage,
		if votage < 6V, system will sleep;
		if votage < power_type gate , system will flash led
	 */
	float A7_value, A7_voltage, battery_voltage;

	A7_value = analogRead(A7);
	A7_voltage = A7_value / 1024 * 5;
	battery_voltage = A7_voltage * 14.7 / 4.7;
	if(BATTERY_DEBUG){
		Serial.print("  System power is ");Serial.print(battery_voltage);Serial.println("V");
	} 

	// system need at least 6V voltage to work, if less then 6v, go to sleep
	if(battery_voltage < 6){		
		if(BATTERY_DEBUG){Serial.println("  System power is less then 6V, and go to sleep");}
		for(int i=0; i<26; i++){
			status_led_ctrl(STATUSLEDOFF);
			delay(100);
			status_led_ctrl(STATUSLEDON);
			delay(100);  
		}
		do_sleep();
	}
	// raspi will tell arduino power_type, every power-type has different alarm gate
	else if(battery_voltage < alarm_gate[power_type]){	
		low_power = true;
	}
	else
		low_power = false;
}

/* when there has data on i2c , recieveData() will run*/
void receive_data(int byte_count) {
	if (I2C_DEBUG) {
		Serial.println("============ Data received! ============");
	}

	while (Wire.available()) {
		number = Wire.read();
	}
	number_flag = 1;

	if (I2C_DEBUG) {
		Serial.print("  Received number = 0x");
		Serial.println(number, HEX);
	}
}

void send_data() {
	if (I2C_DEBUG) {
		Serial.println("============== Data Sent! ==============");
		Serial.print("  Sent value: "); Serial.println(a);
		Serial.println("");
	}
	delay(1);
	Wire.write(a);
}

/* arduino sleep , and turn off other device */
void do_sleep() {
	if (DEBUG) {
		Serial.println("============= Sleep begin! =============");
	}
		servo_switch_ctrl(SERVOPOWEROFF);
		motor_switch_ctrl(MOTORPOWEROFF);
		speaker_switch_ctrl(SPEAKERPOWEROFF);

	/*delay 'SLEEPDELAY' to turn off rpi , because that rpi shut down need sometime */
	if (DEBUG) {                   // if debug , need more time
		Serial.print("  Delay "); Serial.print(SLEEPDELAY);
		Serial.println(" to shut down raspberry pi");
	}
	led_breath_power_off();        // led breath effect
	delay(SLEEPDELAY);
	if (DEBUG) {
		Serial.print("  0. Times up");
	}
	rpi_switch_ctrl(RPIPOWEROFF);
	if (DEBUG) {
		Serial.println("  Raspberry Pi Power is OFF ");
		Serial.println("  Go to sleep.");
	}
	energy.PowerDown();           // Arduino go to sleep
}
