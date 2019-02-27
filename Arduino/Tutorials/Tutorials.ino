#include "Arduino.h"
#include "Rabbit.h"

// the setup function runs once when you press reset or power the board
Rabbit bunny_wabbit;

void setup() {
	Serial.begin(9600);
}


// the loop function runs over and over again forever
void loop() {
	//Serial.print("la");
	Serial.println(bunny_wabbit.do_something());
}
