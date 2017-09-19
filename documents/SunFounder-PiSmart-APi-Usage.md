github repositary: SunFounder\_PiSmart   
Download from Github:
> [https://github.com/sunfounder/SunFounder_PiSmart.git](https://github.com/sunfounder/SunFounder_PiSmart.git)  

<font color=#0000ff face="consolas">pismart</font> stores Python modules  
<font color=#0000ff face="consolas">examples</font> includes some examples for use  

Import package: import pismart  
In the pismart package, the following python modules are included:  
<font color=#0000ff face="consolas">pismart</font>  
├── pismart.py  
├── adc.py  
├── led.py  
├── motor.py  
├── servo.py  
├── pwm.py  
├── tts.py  
├── stt.py  
├── amateur.py  
├── basic.py  

<font color=#0099ff size=6 face="黑体">1.pismart.py</font>  
This file is to control the device switching on and off of the PiSmart, read the temperature and power, and set the speaker and pickup.  
The pismart module includes one class：PiSmart instance creation, with no parameters.  

> 
    from pismart.pismart import PiSmart  
	my_pismart = PiSmart()        # creat an instance


Method functions:  

- **servo\_switch(on\_off)**  
Switch on and off of the servo output.  
Parameters: 1(PiSmart.ON), 0(PiSmart.OFF)  

		my_pismart.servo_switch(PiSmart.ON)    # servo port on
		my_pismart.servo_switch(PiSmart.OFF)   # servo port off

- **motor\_switch(on\_off)**  
Switch on and off of the motor output.  
Parameters: 1(PiSmart.ON), 0(PiSmart.OFF)

		my_pismart.motor_switch(PiSmart.ON)    # motor port on
		my_pismart.motor_switch(PiSmart.OFF)   # motor port off

- **speaker\_switch(on\_off)**   
Switch on and off of the speaker output.  
Parameters: 1(PiSmart.ON), 0(PiSmart.OFF)

		my_pismart.speaker_switch(PiSmart.ON)    # speaker on
		my_pismart.speaker_switch(PiSmart.OFF)   # speaker off

- **power\_voltage**   
Read the voltage of the power, return a float value.  

		bat_voltage = my_pismart.power_voltage   # power voltage

- **power_type**  
Check and set the type of power supply, ranging in ['2S', '3S', 'DC']  

		pwr_type = my_pismart.power_type    # get power type
		my_pismart.power_type = '2S'        # set power type

- **speaker_volume**  
Check and set sound volume of the speaker, ranging between [0-100]

		spk_vol = my_pismart.speaker_volume  # get speaker volume
		my_pismart.speaker_volume = 60       # set speaker volume

- **capture_volume**  
Check and set the boost of the microphone, ranging between [0~100]

		cap_vol = my_pismart.capture_volume  # get capture volume
		my_pismart.capture_volume = 100      # set capture volume

- **cpu_temperature**  
CHeck the temperature of the Raspberry Pi's CPU, returning a float value.

		cpu_temp = my_pismart.cpu_temperature  # get cpu temperature 

- **cpu_usage**  
CHeck the usage of the Raspberry Pi's CPU, returning a float value.

		cpu_usage = my_pismart.cpu_usage    # get cpu usage

<font color=#0099ff size=6 face="黑体">2.adc.py</font>  
Read the value of ADC from the PiSmart bottom plate.  
Create an instance, with a parameter for analog channels, an integer ranging between [0\~4].

> 
    from pismart.adc import ADC  
	my_A0 = ADC(0)  			# creat adc use chn 0
	my_A1 = ADC(1)  			


- **read()**    
Read the analog value of ports, return an integer analog value.   
No parameters. 

		A0_val = my_A0.read()	# get analog val ch.0
		A1_val = my_A1.read()	

- **channel**    
Check and set channels, assignable with values ranging between [0~4]. 

		A0_chn = my_A0.channel  # get channel
		my_A0.channel = 4       # set channel

<font color=#0099ff size=6 face="黑体">3.led.py</font>  

Control the LED ring on top of the PiSmart box.  
The ring consists of 2 groups of LEDs.   
Create an instance, to which a parameter ['led1', 'led2'] can be transferred; the two objects control the two groups of LEDs respectively. Or with no parameters, then it controls the whole ring of LEDs.  

> 
	from pismart.led import LED  
	my_leds = LED()        # creat led object for all leds
	led1 = LED('led1')     # creat led1 object for led1 group
	led2 = LED('led2')

- **brightness**    
Check and set the brightness of the LED. Assignable with integers ranging [0~100]

		led_bri = my_leds.brightness  # get led brightness
		my_leds.brightness = 60       # set led brightness

- **off()**    
Switch off the LED, method function, with no parameters.

		my_leds.off()    # set led off

<font color=#0099ff size=6 face="黑体">4.motor.py</font>  

Control the motor connected to PiSmart.  
Create an instance, with 2 parameters:   
channel ['MotorA','MotorB'], channel of motor output. 
forward [0, 1], direction turning of the motor, 0 by default when no parameter is sent.  

> 
	from pismart.motor import Motor  
	from pismart.pismart import PiSmart
	p = PiSmart()
	motorA = Motor("MotorA")      # creat motor instance
	motorB = Motor("MotorB")
	p.motor_switch(1)             # motor switch on

- **forward\_direction**    
Check and set the forward direction of the motor. Return 0 or 1, also can be set as 0 and 1. 

		direc = motorA.forward_direction  # get motor forward direction
		motorA.forward_direction = 0      # set motor forward direction

- **forward(speed)**    
Drive the motor to go forward in the speed of "speed".   

		motorA.forward(60)     # drive motor forward as speed

- **backward(speed)**    
Drive the motor to go backward in the speed of "speed".  

		motorA.backward(60)    # drive motor backward as speed

- **stop()**    
Drive the motor to stop.   

		motorA.stop()         # motor off

- **speed**    
Set the speed of the motor, ranging between [0~100], integer, with the limited range.   

		motorA.speed = 60     # set motor speed

- **is\_reversed**    
Set the motor to spin reversely, bool type, with warning of wrong types.  

		motorA.is_reversed = True    # set motor turn reversed

- **end()**    
End the motor ojbect.  

		motorA.end()    # motor end

<font color=#0099ff size=6 face="黑体">5.servo.py</font>  

Control the servo connected to PiSmart to spin to a designated angle.   
Create an instance, with 2 parameters:   
channel: integer ranging between [0~7], for pwm0~pwm7 on PiSmart respetively.  
offset: integer ranging between [0~180], offset value of accuracy of the servo spinning.

> 
	from pismart.servo import Servo  
	from pismart.pismart import PiSmart
	p = PiSmart()
	servo1 = Servo(0)       # creat servo with0 ch.0
	p.servo_switch(1)

- **min\_pulse_width**    
Check and set the minimum pulse width. Please set based on the servo specifications.   

		min_p_width = servo1.min_pulse_width  # get min pulse width
		servo1.min_pulse_width = 600    # set min pulse width

- **max\_pulse\_width**    
Check and set the maximum pulse width. Please set based on the servo specifications.   

		max_p_width = servo1.max_pulse_width  # get max pulse width
		servo1.max_pulse_width = 2400   # set max pulse width

- **frequency**    
Check and set the pulse frequency. Please set based on the servo specifications.  

		min_width = servo1.frequency  # get frequency
		servo1.frequency = 60    # set frequency

- **channel**    
Check and set the channel.  

		channel = servo1.channel  # get channel
		servo1.channel = 1      # set channel

- **angle**    
Check and set the angle the servo spins to.   

		angle = servo1.angle    # get angle
		servo1.angle = 90    # set angle

- **offset**    
Offset value for the servo spinning. It is the pwm pulse width, ranging between [-4096, 4096].  

		offset = servo1.offset   # get servo offset
		servo1.offset = 120      # set servo offset


- **turn(angle)**    
Drive the servo to spin to a designated angle.   
Transfer integer parameter for the angle, ranging between [0 ~ 180].  

		servo1.turn(90)     # turn to angle

<font color=#0099ff size=6 face="黑体">6.pwm.py</font>  

Control the pin pwm0~pwm7 to output pwm signals.  
Generally to control the brightness of the LED. Please DO NOT drive servo directly with the pwm module.  

> 
	from pismart.pwm import PWM  
	from pismart.pismart import PiSmart
	p = PiSmart()
	pwm = PWM(0)          # create pwm
	p.servo_switch(1)

- **channel**    
Check and set the channel, ranging between [0-7].  

		chn = pwm.channel  # get channel
		pwm.channel = 1    # set channel

- **frequency**    
Check and set the frequency.  

		freq = pwm.frequency  # get pwm frequency
		pwm.frequency = 60    # set pwm frequency

- **set_PWM(on, off=0)**    
Set the time period for high and low levels of PWM, ranging between [0, 4095]. 

		pwm.set_PWM = 2048  # set pwm on_time

- **value**    
Set and acquire the time of high and low levels of PWM. 

		pwm_on_time = pwm.value  # get pwm on_time
		pwm.value = 2048    # set pwm on_time


<font color=#0099ff size=6 face="黑体">7.tts.py</font>  

Convert the text into speech broadcast.   

Create an instance, with a parameter engine for selecting the speech engine of broadcasting from available ['festival', 'espeak', 'pico']; 'pico' by default if no engine is choosen.


> 
	from pismart.tts import TTS  
	from pismart.pismart import PiSmart
	p = PiSmart()
	tts = TTS('pico')       # create tts
	p.speaker_volume(100)

- **say**    
Make the PiSmart broadcast the speech set.  
Assign strings.  

		tts.say = "Hello, world!"   # say words

- **engine**    
Check and set the speech engine.  
Values available: ['festival', 'espeak', 'pico'].  

		engine = tts.engine    # get tts engine
		tts.engine = "espeak"  # set tts engine

- **engine_pa
- rams(amp=None, speed=None, gap=None, pitch=None)**    
Set the parameters of the engine. Available only when the espeak engine is selected.
Four parameters:   
amp=None, amp should be in 0 to 200  
speed=None, speed should be in 80 to 260
gap=None  
pitch=None, pitch should be in 0 to 99

		tts.engine = "espeak"      # set espeak
		tts.espeak_params(speed = 150)  


<font color=#0099ff size=6 face="黑体">8.stt.py</font>  
Convert speech into text for PiSmart, used in speech recognition.  
Create an instance, parameters should be transferred: (dictionary, device=1, name_calling=False, timeout=5.0, dictionary_update=False).  
dictionary: File name of the dictionary under the same directory of the script.  
device: Number of the sound card devices for the Raspberry Pi in PiSmart, 1 by default. If other sound cards are used, assign a parameter based on the device number. 
name\_calling: Whether to turn on awaking by speaking the name, ranging in [True, False].
timeout: Time of timeout to end awaking since no command is heard after name_calling.   
dictionary\_update: Whether to update the dictionary. The update can generate essential dictionaries and intermediate files needed for speech recognition. 

> 
	from pismart.tts import TTS  
	from pismart.pismart import PiSmart
	p = PiSmart()
	stt = STT('dictionary', name_calling=True, timeout=10.0, dictionary_update=True)
	p.speaker_volume(100)

- **is\_awake**    
Whether to be awakened. If it's awakened by its name, return True. Need to open name_calling when the object is created. 

		if stt.is_awake:  # need name_calling True
		    xxxx  

- **heard**    
If some speech is heard, return True.    

		if stt.heard:    # if heard do something
		    xxxx

- **recognize()**    
Enter the process of speech recognition. No parameters, no values returned.    

		while True:  
		    stt.recognize()    # begin recognize

- **update_dictionary()**    
Update the dictionary file. No parameters, return the value 0.    

		stt.update_dictionary()   # update dictionary

- **end()**    
End the process of speech recognition.No parameters, no values returned.     

		stt.end()

An instance:

		from pismart.pismart import PiSmart
		from pismart.stt import STT
		from pismart.tts import TTS
		
		p = PiSmart()  
		sr = STT('dictionary', name_calling=True, timeout=10.0, dictionary_update=True)  
		p.speaker_switch(1)

		pico = TTS('pico')


	    while True:
	        sr.recognize()
	        print "heard :%s"%sr.heard
	        if sr.heard:
	            result = sr.result
	            print "=============================="
	            print result
	            print "=============================="
	            if result == '__NAME__':
	                pico.say = 'Hello there'
	            else:
	                pico.say = result


<font color=#0099ff size=6 face="黑体">9.amateur.py</font>  
Integration module. The amateur file integrates most of the control part for PiSmart, though the debugging and customization is not deep enough. 

> 
    from pismart.amateur import PiSmart  
	my_pismart = PiSmart()  

- **xxx_init()**    
Initialize resources on the PiSmart, with no parameters. When the amateur instance is created, all the initialization will be executed. 

		my_pismart.ADC_init()  
		my_pismart.Motor_init()
		my_pismart.PWM_init()
		my_pismart.Servo_init()
		my_pismart.LED_init()
		my_pismart.TTS_init()
		my_pismart.STT_init()
		my_pismart.All_init()

- **xxx_end()**    
End the processing of the resources on PiSmart. No parameters. 

		my_pismart.ADC_end()  
		my_pismart.Motor_end()
		my_pismart.PWM_end()
		my_pismart.Servo_end()
		my_pismart.LED_end()
		my_pismart.TTS_end()
		my_pismart.STT_end()
		my_pismart.end()

- **power_type**    
Power type, assignable with value in ['2S', '3S', 'DC']. 

		my_pismart.power_type = '2S'  

- **power_voltage**    
Power voltage, returning a float value, unassignable. 

		power_voltage = my_pismart.power_voltage 

- **speaker_volume**    
Set the sound volume of the speaker, assignable with value in [0 ~ 100].

		my_pismart.speaker_volume = 60

- **capture_volume**  
Boost of microphone, assignable with value in [0 ~ 100].

		my_pismart.capture_volume = 100

- **cpu_temperature**  
Temperature of the Raspberry Pi's CPU, returning a float value.

		cpu_temp = my_pismart.cpu_temperature 

- **A0 ~ A4**  
Values returned from analog pins A0~A4. Return integer values, unassignable.

		A0_val = my_pismart.A0  
		A1_val = my_pismart.A1  

- **Servo0 ~ Servo7**  
Output angles of servo when any servo is connected to pin pwm0~pwm7, assignable with value in [0 ~ 180].

		my_pismart.Servo0 = 90 
		my_pismart.Servo1 = 0 


- **PWM0 ~ PWM7**  
Output duty cycle of pwm0~pwm7, assignable with value in [0 ~ 100].

		my_pismart.Servo0 = 30 
		my_pismart.Servo1 = 90 

- **LED**  
Brightness of the LEDs on top of the PiSmart, assignable with value in [0 ~ 100].

		my_pismart.LED = 30 
		my_pismart.LED = 90 

- **MotorA 和 MotorB**  
Rotating speed of the MotorA and MotorB, assignable with value in [0 ~ 100].

		my_pismart.MotorA = 30 
		my_pismart.MotorB = 90 

- **MotorA\_reversed 和 MotorB\_reversed**  
Rotating direction of the MotorA and MotorB, assignable with value in [True， False].

		my_pismart.MotorA_reversed = False 
		my_pismart.MotorB_reversed = True 

- **Say**  
Speech of the PiSmart, assigned with texts which the PiSmart will say.

		my_pismart.Say = "Hello, world!"  

- **listen**  
PiSmart will enter the process of listening, unassignable. 

		my_pismart.listen 

- **heard**  
PiSmart is in the process of listening. Return True if any speech is heard. Unassignable.

		if my_pismart.heard:
		    xxxx 

- **result**  
After PiSmart heard something, result will acquire what's heard. Unassignable.

		if my_pismart.result == "forward":
		    xxxx

An instance:  

		def loop():
			my_pismart.listen    # Begin to listen
			if my_pismart.heard:    # if heard something
				if my_pismart.result == "forward":  # if heard forward 
					# PiSmart Car move forward
					my_pismart.MotorA = 60
					my_pismart.MotorB = 60
					my_pismart.Say = "I go forward!"
					sleep(3) 	

