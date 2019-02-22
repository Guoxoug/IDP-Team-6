/*
 * Rabbit.cpp
 *
 *  Created on: 21 Feb 2019
 *      Author: Guy
 */

#include "Rabbit.h"
#include "Arduino.h" // for serial

String Rabbit::do_something() {
	Serial.println("rabbit rabbit rabbit");
	return "boinggg";
}
