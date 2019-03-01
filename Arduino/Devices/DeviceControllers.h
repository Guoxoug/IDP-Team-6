/*
 * DeviceControllers.h
 *
 *  Created on: 27 Feb 2019
 *      Author: Guy
 */

#ifndef DEVICECONTROLLERS_H_
#define DEVICECONTROLLERS_H_

#include "Adafruit_MotorShield.h"

extern Adafruit_MotorShield AFMS;

class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number);
	int pin;
	void print_device_location();
	virtual void set_state(int power) = 0;
};

class Sensor: public IO {
	//base class extends IO to make it output a value
private:
	int old_state = 0; //everything starts off :)

public:
	Sensor(int pin);
	virtual int read_state() = 0;
	bool state_changed();
};



class LED: public IO {//subclass IO
public:
	LED(int pin_number);
	void set_state(int power);
};



class DCMotor: public IO {
private:
	int direction;
public:
	DCMotor(int motor_port, int direction);
	void set_state(int power);
	Adafruit_DCMotor *motor;
};

#endif /* DEVICECONTROLLERS_H_ */
