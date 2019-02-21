#include "Arduino.h"
//#include "Chicken.h"


// the setup function runs once when you press reset or power the board
int the_led = LED_BUILTIN;

void setup() {
  // Initialise digital pin LED_BUILTIN as an output.
  pinMode(the_led, OUTPUT);

}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(the_led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(the_led, LOW);    // turn the LED off by making the voltage LOW
  delay(100);                       // wait for a second
  //bleep();
  Serial.println("oaf");
}
