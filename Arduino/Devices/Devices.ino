#include "Arduino.h"
#include "DeviceControllers.h"

//IO genericIO = new IO(LED_BUILTIN);
LED* led;
DCMotor* right_fwd;
Button* push_button;

void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
  AFMS.begin();

  led = new LED(LED_BUILTIN); //these declarations must come after Serial & AFMS
  led->print_device_location();
  right_fwd = new DCMotor(1,FORWARD);
  right_fwd->print_device_location();
  push_button = new Button(2);
}

void loop() {
	//genericIO.print_pin_state();
	//do some blinking
	led->set_state(HIGH);
	delay(1000);
	led->set_state(LOW);
	delay(1000);

	//do some motoring

	int i;
	Serial.println("tick");

	led->set_state(HIGH);
	for (i=0; i<255; i++) {
		right_fwd->set_state(i);
		delay(10);
	}
	led->set_state(LOW);
	for (i=255; i!=0; i--) {
		right_fwd->set_state(i);
		delay(10);
	}
}
