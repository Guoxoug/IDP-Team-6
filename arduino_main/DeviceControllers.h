/*
 * DeviceControllers.h
 *
 *  Created on: 27 Feb 2019
 *      Author: Guy
 */

#ifndef DEVICECONTROLLERS_H_
#define DEVICECONTROLLERS_H_

#include "Adafruit_MotorShield.h"
#include <Servo.h>
extern Adafruit_MotorShield AFMS;

class IO {
	//Base class to define any sort of input/output by associating it with a pin
public:
	IO(int pin_number);
	int pin;
	void print_pin_state();
	virtual void set_state(int power) = 0;
};


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
};
class IDP_servo: public IO {

public:
	IDP_servo(int pin_number);
	void set_state(int position);
	Servo our_servo;

};
#endif /* DEVICECONTROLLERS_H_ */
