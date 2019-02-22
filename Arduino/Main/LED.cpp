/*
 * LED.cpp
 *
 *  Created on: 22 Feb 2019
 *      Author: Guy
 */

#include "LED.h"
#include "Arduino.h"

void flash_builtin(int period = 1000, int n_flashes = 5) {
	LED light(LED_BUILTIN);
	for(int i = 0; i < n_flashes*2; i++) {
		light.toggle();
		delay(period);
	}

}

void LED::set_state(int new_state) {
	state = new_state;
	digitalWrite(pin_number, new_state);
}

void LED::toggle() {
	LED::set_state(!state);
}

LED::LED(int pin_n) {
	pinMode(pin_n, OUTPUT);
	set_state(false); //default on
	pin_number = pin_n;
}

