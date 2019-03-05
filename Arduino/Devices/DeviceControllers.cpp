/*
 * DeviceControllers.cpp
 *
 *  Created on: 27 Feb 2019
 *      Author: Guy
 */

#include "DeviceControllers.h"
#include "Arduino.h"
#include "Adafruit_MotorShield.h"

const int max_arg = 8;
Adafruit_MotorShield AFMS = Adafruit_MotorShield();


IO::IO(int pin_number){ //Parameterised constructor for generic IO
	pin = pin_number;
	Serial.println("IO constructor");
}

void IO::print_device_location(){
	Serial.print("IO is located on pin/port: ");
	Serial.println(pin);
}

Sensor::Sensor(int pin_number) : IO(pin_number){
	pinMode(pin, INPUT);//works if we switch to OUTPUT
}

bool Sensor::state_changed(){ //default state changed check is pretty literal
	//if this works I'll be very impressed, considering read_state isn't defined yet
	int new_state = read_state();
	bool state_changed = (old_state != new_state);
	old_state = new_state; //save for next time
	return state_changed;
}

Button::Button(int pin_number) : Sensor(pin_number){}


int Button::read_state(){
	return digitalRead(pin);
}

LED::LED(int pin_number) : IO(pin_number){
	Serial.println("LED constructor");
	pinMode(pin, OUTPUT);
}

void LED::set_state(int val){//Expects Low or High, 0 or 1
	//int digital_state = map( val, 0, max_arg, 0, 1);
	digitalWrite(pin, val);
}

DCMotor::DCMotor(int motor_port, int dir) : IO(motor_port){
	motor = AFMS.getMotor(motor_port);
	direction = dir;
}

<<<<<<< master
<<<<<<< master
void DCMotor::set_state(int power){
=======
void DCMotor::set_power(int power){
>>>>>>> Fix motor definition
=======
void DCMotor::set_state(int power){
>>>>>>> Refactor name of function
	motor->setSpeed(power);
	motor->run(direction);
}
