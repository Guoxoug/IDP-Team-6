#include "LED.h"
#include "Arduino.h"

// the setup function runs once when you press reset or power the board

LED light = new LED(LED_BUILTIN);

void setup() {
  // Initialise digital pin 13 as an output.

}

// the loop function runs over and over again forever
void loop() {
	light.toggle();
	delay(1000);
}
