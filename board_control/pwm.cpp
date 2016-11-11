#include "pwm.h"

int read_byte(int addr) {
  Wire.beginTransmission(PWM_ADDRESS);
  Wire.write(addr);
  Wire.endTransmission();

  Wire.requestFrom((int)PWM_ADDRESS, (int)1);
  return Wire.read();
}

void writeByte(int addr, int d) {
  Wire.beginTransmission(PWM_ADDRESS);
  Wire.write(addr);
  Wire.write(d);
  Wire.endTransmission();
}

void pwmBegin() {
  Wire.begin();
  writeByte(PCA9685_MODE1, 0x0);
}

void pwmSetFrequency(float freq) {
  //Serial.print("Attempting to set freq ");
  //Serial.println(freq);
  freq *= 0.9;  // Correct for overshoot in the frequency setting (see issue #11).
  float preScaleValue = 25000000;
  preScaleValue /= 4096;
  preScaleValue /= freq;
  preScaleValue -= 1;
  if (PWM_DEBUG) {
  Serial.print("Estimated pre-scale: "); Serial.println(preScaleValue);
  }
  int preScale = floor(preScaleValue + 0.5);
  if (PWM_DEBUG) {
  Serial.print("Final pre-scale: "); Serial.println(preScale);
  }

  int oldMode = read_byte(PCA9685_MODE1);
  int newMode = (oldMode & 0x7F) | 0x10; // sleep
  writeByte(PCA9685_MODE1, newMode); // go to sleep
  writeByte(PCA9685_PRESCALE, preScale); // set the prescaler
  writeByte(PCA9685_MODE1, oldMode);
  delay(5);
  writeByte(PCA9685_MODE1, oldMode | 0xa1);  //  This sets the MODE1 register to turn on auto increment.
  // This is why the beginTransmission below was not working.
  //  Serial.print("Mode now 0x"); Serial.println(read_byte(PCA9685_MODE1), HEX);
}

void pwmSetValue(int num, int on, int off) {
  //Serial.print("Setting PWM "); Serial.print(num); Serial.print(": "); Serial.print(on); Serial.print("->"); Serial.println(off);

  Wire.beginTransmission(PWM_ADDRESS);
  Wire.write(LED0_ON_L + 4 * num);
  Wire.write(on);
  Wire.write(on >> 8);
  Wire.write(off);
  Wire.write(off >> 8);
  Wire.endTransmission();
}
