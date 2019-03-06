#include "Arduino.h"
#include "DeviceControllers.h"
#include "Vector.h"


//IO genericIO = new IO(LED_BUILTIN);
LED* led;
DCMotor* right_fwd;
Button* push_button;
Vector<IO> outputs;

void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
  AFMS.begin();

  led = new LED(LED_BUILTIN); //these declarations must come after Serial & AFMS
  led->print_device_location();
//  right_fwd = new DCMotor(1,FORWARD);
//  right_fwd->print_device_location();
  push_button = new Button(2);
  push_button->print_device_location();

}

void loop() {
	//read button state

	if (push_button->state_changed()){ //needs debouncing
		Serial.println("boop");
		led->set_state(push_button->read_state());
	}


}
