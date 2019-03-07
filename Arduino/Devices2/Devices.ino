#include "Arduino.h"
#include "DeviceControllers.h"
#include "Vector.h"


//IO genericIO = new IO(LED_BUILTIN);
LED* led;
DCMotor* right_fwd;
Button* push_button;

void setup() {
	Serial.begin(9600);           //Start serial and set the correct Baud Rate
	AFMS.begin();
	led = new LED(LED_BUILTIN); //these declarations must come after Serial
	led->print_device_location();
	right_fwd = new DCMotor(1,FORWARD);
	right_fwd->print_device_location();
	push_button = new Button(2);

}

void loop() {
	//genericIO.print_pin_state();
	//do some blinking
	//led->set_state(push_button->read_state());


	if (push_button->state_changed()){
		led->set_state(HIGH);
		delay(1000);
		led->set_state(LOW);
		delay(1000);
	}
}
