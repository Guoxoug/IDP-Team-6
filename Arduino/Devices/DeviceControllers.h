/*
 * DeviceControllers.h
 *
 *  Created on: 27 Feb 2019
 *      Author: Guy
 */

#ifndef DEVICECONTROLLERS_H_
#define DEVICECONTROLLERS_H_

#include "Adafruit_MotorShield.h"

class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number);
	int pin;
	void print_pin_state();
	virtual void set_power(int power) = 0;
};


class LED: public IO {//subclass IO
public:
	LED(int pin_number);
	void set_power(int power);
};

class DCMotor: public IO {
private:
	int direction;
public:
	DCMotor(int motor_port, int direction);
	void set_power(int power);
	Adafruit_DCMotor *motor;
};

#endif /* DEVICECONTROLLERS_H_ */
