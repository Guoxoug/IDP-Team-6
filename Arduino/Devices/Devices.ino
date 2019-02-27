#include "Arduino.h"

const int max_arg = 8;

class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number);
	int pin;
	void print_pin_state();
	virtual void set_power(int val) = 0;
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
	void set_power(int val);
};

LED::LED(int pin_number) : IO(pin_number){
	Serial.println("LED constructor");
	pinMode(pin, OUTPUT);
}

void LED::set_power(int val){//Expects Low or High, 0 or 1
	//int digital_state = map( val, 0, max_arg, 0, 1);
	digitalWrite(pin, val);
}

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
