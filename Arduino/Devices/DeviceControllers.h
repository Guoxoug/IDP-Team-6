/*
 * DeviceControllers.h
 *
 *  Created on: 27 Feb 2019
 *      Author: Guy
 */

#ifndef DEVICECONTROLLERS_H_
#define DEVICECONTROLLERS_H_


class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number);
	int pin;
	void print_pin_state();
	virtual void set_power(int val) = 0;
};


class LED: public IO { //Subclass IO
public:
	LED(int pin_number); //default on
	void set_power(int val);
};

#endif /* DEVICECONTROLLERS_H_ */
