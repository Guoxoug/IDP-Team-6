/*
 * LED.h
 *
 *  Created on: 22 Feb 2019
 *      Author: Guy
 */

#ifndef DEVICES_H_
#define DEVICES_H_

#include "Arduino.h"

void flash_builtin(int period = 1000, int n_flashes = 5);

class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number): pin(pin_number){;} //Parameterised constructor, used to set pin
	void print_pin_info() {Serial.println(pin);}
	int pin;
};

class LED: public IO { //Subclass IO
private:
	bool state;

public:
	LED(int pin_number): IO(pin_number){
		pinMode(pin, OUTPUT);
		set_state(state); //default on
	}
	void set_state(int new_state);
	void toggle();

};

#endif /* DEVICES_H_ */
