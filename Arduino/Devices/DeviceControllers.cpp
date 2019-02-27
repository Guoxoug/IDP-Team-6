/*
 * DeviceControllers.cpp
 *
 *  Created on: 27 Feb 2019
 *      Author: Guy
 */

#include "DeviceControllers.h"
#include "Arduino.h"

const int max_arg = 8;

IO::IO(int pin_number){ //Parameterised constructor for generic IO
	pin = pin_number;
	Serial.println("IO constructor");
}

void IO::print_pin_state(){
	Serial.println(pin);
}

LED::LED(int pin_number) : IO(pin_number){
	Serial.println("LED constructor");
	pinMode(pin, OUTPUT);
}

void LED::set_power(int val){//Expects Low or High, 0 or 1
	//int digital_state = map( val, 0, max_arg, 0, 1);
	digitalWrite(pin, val);
}
