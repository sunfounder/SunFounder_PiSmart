#include "led.h"
#include "pwm.h"


void breath_bak(int startValue, int endValue, int led){
  startValue = map(startValue, 0, 100, 0, 157);
  endValue = map(endValue, 0, 100, 0, 157);
  int step;

  if (startValue > endValue)
    step = -1;
  else
    step = 1;

  if (LED_DEBUG) {
    Serial.print("step = "); Serial.println(step);
    Serial.print(startValue); Serial.print("->"); Serial.println(endValue);
  }

  double brightness;
  float tmp;
  for (int i = startValue; i != endValue; i=i+step)
  {
    tmp = float(i) / 100;
    brightness = 100 * sin(tmp);
    brightness = map(brightness, 0, 100, 0, 4095);
    pwmSetValue(led, 0, brightness);
    delay(BREATH_DELAY);
  }
}


void breath(int startValue, int endValue, int led){
  startValue = map(startValue, 0, 100, 0, 157);
  endValue = map(endValue, 0, 100, 0, 157);
  int step;

  if (startValue > endValue)
    step = -1;
  else
    step = 1;

  if (LED_DEBUG) {
    Serial.print("step = "); Serial.println(step);
    Serial.print(startValue); Serial.print("->"); Serial.println(endValue);
  }

  double brightness;
  float tmp;
  for (int i = startValue; i != endValue; i=i+step)
  {
    tmp = float(i) / 100;
    brightness = 100 * sin(tmp);
    brightness = map(brightness, 0, 100, 0, 4095);
    pwmSetValue(RED, 0, brightness);
    pwmSetValue(BLUE, 0, brightness);
    delay(BREATH_DELAY);
  }
}
/**
   when wake up and go sleep , arduino will be master ,and contral led breath
*/

/*  x axis means time , y axis means brightness ,
    we set brightness , and then caculate the time stamps
    change the brightness via pwm with time pass by
*/
void breathLedSetup(){
  Wire.endTransmission(true);
  pwmBegin();
  pwmSetFrequency(60);

  pwmSetValue(BLUE, 0, OFF);   //when pi poweroff , we use RED led
  pwmSetValue(RED, 0, OFF);   //when pi poweroff , we use RED led
}

void ledBreathPowerOn() {

  Wire.endTransmission(true);
  pwmBegin();
  pwmSetFrequency(60);
  pwmSetValue(RED, 0, OFF);   //when pi poweron , we use BLUE led

  // OFF  -> BRIGHT ++
  breath(OFF, BRIGHT, BLUE);

  //loop
  for (int i = 0; i < 3; i++) {
    // BRIGHT -> DIMING --
    breath(BRIGHT, DIMING, BLUE);
    // DIMING -> BRIGHT ++
    breath(DIMING, BRIGHT, BLUE);
  }

  // RUNING -> OFF --
  breath(BRIGHT, OFF, BLUE);

  Wire.endTransmission(true);
}

void ledBreathPowerOff() {

  Wire.endTransmission(true);
  pwmBegin();
  pwmSetFrequency(60);

  pwmSetValue(BLUE, 0, OFF);   //when pi poweroff , we use RED led

  // OFF  -> RUNING ++
  breath(OFF, RUNING, RED);

  //LOOP
  for (int i = 0; i < 3; i++) {
    // RUNING -> DIMING --
    breath(RUNING, DIMING, RED);

    // DIMING -> RUNING ++
    breath(DIMING, RUNING, RED);
  }

  // RUNING -> OFF --
  breath(RUNING, OFF, RED);
  pwmSetValue(RED, 0, OFF);   //when pi poweroff , we use RED led
}

void powerOffLedBreathUp() {
  // OFF  -> RUNING ++
  breath(OFF, RUNING, RED);
}

void powerOffLedBreathDown() {
  // OFF  -> RUNING ++
  breath(RUNING, OFF, RED);
}