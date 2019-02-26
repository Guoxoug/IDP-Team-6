/*
 * LED.h
 *
 *  Created on: 22 Feb 2019
 *      Author: Guy
 */

#ifndef LED_H_
#define LED_H_

void flash_builtin(int period = 1000, int n_flashes = 5);

class LED {
public:
	LED(int pin_number);
	void set_state(int new_state);
	void toggle();
private:
	int pin_number;
	bool state;
};

#endif /* LED_H_ */
