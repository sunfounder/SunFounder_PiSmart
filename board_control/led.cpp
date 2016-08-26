#include "led.h"
#include "pwm.h"


void breath(int start_value, int end_value, int led){
  start_value = map(start_value, 0, 100, 0, 157);
  end_value = map(end_value, 0, 100, 0, 157);
  int step;

  if (start_value > end_value)
    step = -1;
  else
    step = 1;

  if (LED_DEBUG) {
    Serial.print("step = "); Serial.println(step);
    Serial.print(start_value); Serial.print("->"); Serial.println(end_value);
  }

  double brightness;
  float tmp;
  for (int i = start_value; i != end_value; i=i+step)
  {
    tmp = float(i) / 100;
    brightness = 100 * sin(tmp);
    brightness = map(brightness, 0, 100, 0, 4095);
    pwm_set_value(led, 0, brightness);
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

void led_breath_power_on() {

  Wire.endTransmission(true);
  pwm_begin();
  pwm_set_frequency(60);
  pwm_set_value(RED, 0, OFF);   //when pi poweron , we use BLUE led

  // OFF  -> BRIGHT ++
  breath(OFF, BRIGHT, BLUE);

  // BRIGHT -> DIMING --
  breath(BRIGHT, DIMING, BLUE);

  //loop
  for (int i = 0; i < 2; i++) {
	// DIMING -> BRIGHT ++
	breath(DIMING, BRIGHT, BLUE);
	// BRIGHT -> DIMING --
	breath(BRIGHT, DIMING, BLUE);
  }
  // DIMING -> RUNING ++
  breath(DIMING, RUNING, BLUE);

  // RUNING -> OFF --
  breath(RUNING, OFF, BLUE);

  Wire.endTransmission(true);
}

void led_breath_power_off() {

  Wire.endTransmission(true);
  pwm_begin();
  pwm_set_frequency(60);

  pwm_set_value(BLUE, 0, OFF);   //when pi poweroff , we use RED led

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
  pwm_set_value(RED, 0, OFF);   //when pi poweroff , we use RED led
}