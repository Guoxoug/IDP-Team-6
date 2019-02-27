#include "Arduino.h"
#include "DeviceControllers.h"

//IO genericIO = new IO(LED_BUILTIN);
LED* led;

void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
  led = new LED(LED_BUILTIN);
  led->print_pin_state();

}

void loop() {
	//genericIO.print_pin_state();
	//do some blinking
	led->set_power(HIGH);
	delay(1000);
	led->set_power(LOW);
	delay(1000);
}
