#include "Arduino.h"
#include "DeviceControllers.h"

//IO genericIO = new IO(LED_BUILTIN);
LED* led;
DCMotor* right_fwd;


void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
  AFMS.begin();
  led = new LED(LED_BUILTIN);
  led->print_pin_state();
  right_fwd = new DCMotor(1,FORWARD);
  right_fwd->print_pin_state();
}

void loop() {
	//genericIO.print_pin_state();
	//do some blinking
//	led->set_power(HIGH);
//	delay(1000);
//	led->set_power(LOW);
//	delay(1000);

	//do some motoring

	uint8_t i;

	Serial.println("tick");

	led->set_power(HIGH);
	for (i=0; i<255; i++) {
		right_fwd->set_power(i);
		delay(10);
	}
	led->set_power(LOW);
	for (i=255; i!=0; i--) {
		right_fwd->set_power(i);
		delay(10);
	}
}
