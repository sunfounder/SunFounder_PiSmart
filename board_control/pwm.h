
#include <Wire.h>
#include <Arduino.h>

#define PWM_DEBUG true   // DEBUG = true,print message
#define PWM_ADDRESS  		0x40

#define PCA9685_MODE1 		0x0
#define PCA9685_PRESCALE 	0xFE
#define LED0_ON_L 			0x6


int readByte(int addr);

void writeByte(int addr, int d);

void pwmBegin();

void pwmSetFrequency(float freq);

void pwmSetValue(int num, int on, int off);
