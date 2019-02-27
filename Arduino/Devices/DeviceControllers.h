/*
 * DeviceControllers.h
 *
 *  Created on: 27 Feb 2019
 *      Author: Guy
 */

#ifndef DEVICECONTROLLERS_H_
#define DEVICECONTROLLERS_H_

#include "Adafruit_MotorShield.h"
<<<<<<< master
#include "Adafruit_MotorShield.h"

extern Adafruit_MotorShield AFMS;
=======
>>>>>>> Extract device controlling into separate files

class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number);
	int pin;
	void print_pin_state();
	virtual void set_power(int power) = 0;
<<<<<<< master
	virtual void set_state(int power) = 0;
};


class LED: public IO {//subclass IO
class LED: public IO {//subclass IO
public:
	LED(int pin_number);
	void set_state(int power);
};

class Button: public IO {//subclass IO
public:
	Button(int pin_number);
	void set_state(int power);
};

class DCMotor: public IO {
private:
	int direction;
public:
	DCMotor(int motor_port, int direction);
	void set_state(int power);
	Adafruit_DCMotor *motor;
=======
	virtual void set_power(int val) = 0;
};


class LED: public IO { //Subclass IO
public:
	LED(int pin_number);
	void set_power(int power);
};
	LED(int pin_number); //default on
	void set_power(int val);
>>>>>>> Extract device controlling into separate files
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
