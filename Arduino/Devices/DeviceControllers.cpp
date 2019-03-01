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

void DCMotor::set_state(int power){
	motor->setSpeed(power);
	motor->run(direction);
}
