#include "Arduino.h"
#include "Devices.h"

// the setup function runs once when you press reset or power the board

LED light = new LED(LED_BUILTIN);

void setup() {
  // Initialise digital pin 13 as an output.
	Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
//	light.toggle();
//	delay(1000);
	flash_builtin();
	flash_builtin(100, 10); //just seems to be repeatedly running the constructors :/
}
