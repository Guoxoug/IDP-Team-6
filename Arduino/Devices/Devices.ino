#include "Arduino.h"

class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number);
	int pin;
	void print_pin_state();
	void set_power(int val);
};

IO::IO(int pin_number){ //Parameterised constructor for generic IO
	pin = pin_number;
	Serial.println("IO constructor");
}

void IO::print_pin_state(){
	Serial.println(pin);
}


class LED: public IO { //Subclass IO
public:
	LED(int pin_number); //default on
};

LED::LED(int pin_number) : IO(pin_number){
	Serial.println("LED constructor");
	pinMode(pin, OUTPUT);
}

//IO genericIO = new IO(LED_BUILTIN);
LED led = new LED(LED_BUILTIN);

void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
  led.print_pin_state();
}

void loop() {
	//genericIO.print_pin_state();
}
