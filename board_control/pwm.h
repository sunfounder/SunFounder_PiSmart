
#include <Wire.h>
#include <Arduino.h>

#define PWM_DEBUG true   // DEBUG = true,print message
#define PWM_ADDRESS  		0x40

#define PCA9685_MODE1 		0x0
#define PCA9685_PRESCALE 	0xFE
#define LED0_ON_L 			0x6


int read_byte(int addr);

void write_byte(int addr, int d);

void pwm_begin();

void pwm_set_frequency(float freq);

void pwm_set_value(int num, int on, int off);
