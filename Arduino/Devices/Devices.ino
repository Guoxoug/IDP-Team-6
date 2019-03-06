#include "Arduino.h"
<<<<<<< master
#include "DeviceControllers.h"
=======

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
>>>>>>> Clean up virtual function

void LED::set_power(int val){//Expects Low or High, 0 or 1
	//int digital_state = map( val, 0, max_arg, 0, 1);
	digitalWrite(pin, val);
}

//IO genericIO = new IO(LED_BUILTIN);
LED* led;
DCMotor* right_fwd;


void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
  AFMS.begin();
  led = new LED(LED_BUILTIN); //these declarations must come after Serial
  led->print_pin_state();
  right_fwd = new DCMotor(1,FORWARD);
  right_fwd->print_pin_state();
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
