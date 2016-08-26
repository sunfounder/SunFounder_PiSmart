#include "pwm.h"

int read_byte(int addr) {
  Wire.beginTransmission(PWM_ADDRESS);
  Wire.write(addr);
  Wire.endTransmission();

  Wire.requestFrom((int)PWM_ADDRESS, (int)1);
  return Wire.read();
}

void write_byte(int addr, int d) {
  Wire.beginTransmission(PWM_ADDRESS);
  Wire.write(addr);
  Wire.write(d);
  Wire.endTransmission();
}

void pwm_begin() {
  Wire.begin();
  write_byte(PCA9685_MODE1, 0x0);
}

void pwm_set_frequency(float freq) {
  //Serial.print("Attempting to set freq ");
  //Serial.println(freq);
  freq *= 0.9;  // Correct for overshoot in the frequency setting (see issue #11).
  float prescaleval = 25000000;
  prescaleval /= 4096;
  prescaleval /= freq;
  prescaleval -= 1;
  if (PWM_DEBUG) {
  Serial.print("Estimated pre-scale: "); Serial.println(prescaleval);
  }
  int prescale = floor(prescaleval + 0.5);
  if (PWM_DEBUG) {
  Serial.print("Final pre-scale: "); Serial.println(prescale);
  }

  int oldmode = read_byte(PCA9685_MODE1);
  int newmode = (oldmode & 0x7F) | 0x10; // sleep
  write_byte(PCA9685_MODE1, newmode); // go to sleep
  write_byte(PCA9685_PRESCALE, prescale); // set the prescaler
  write_byte(PCA9685_MODE1, oldmode);
  delay(5);
  write_byte(PCA9685_MODE1, oldmode | 0xa1);  //  This sets the MODE1 register to turn on auto increment.
  // This is why the beginTransmission below was not working.
  //  Serial.print("Mode now 0x"); Serial.println(read_byte(PCA9685_MODE1), HEX);
}

void pwm_set_value(int num, int on, int off) {
  //Serial.print("Setting PWM "); Serial.print(num); Serial.print(": "); Serial.print(on); Serial.print("->"); Serial.println(off);

  Wire.beginTransmission(PWM_ADDRESS);
  Wire.write(LED0_ON_L + 4 * num);
  Wire.write(on);
  Wire.write(on >> 8);
  Wire.write(off);
  Wire.write(off >> 8);
  Wire.endTransmission();
}
