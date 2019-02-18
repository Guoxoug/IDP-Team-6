// the setup function runs once when you press reset or power the board
int the_led = 4;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(the_led, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(the_led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(the_led, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}
