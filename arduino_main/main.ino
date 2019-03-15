// using serialEvent(), called at the end of each loop (called when data is available)


#include "Arduino.h"
#include "DeviceControllers.h"
#include "Adafruit_MotorShield.h"
#include <Servo.h>

DCMotor* right_fwd;
DCMotor* right_bwd;
DCMotor* left_fwd;
DCMotor* left_bwd;
DCMotor* pulley_up;
DCMotor* pulley_down;
DCMotor* pusher_out;
DCMotor* pusher_in;
Button* hall_effect1;
Button* hall_effect2;
Button* IR_sensor;
IDP_servo* selector_servo;
LED* drive_led;
LED* hall_led;
LED* IR_led;

void establishContact();
String input_command = "";         // a String to hold incoming data
bool string_complete = false;  // whether the string is complete

void setup() {
	AFMS.begin();   // create with the default frequency 1.6KHz

	// I/O object definitions
	//Motors and servos
  drive_led = new LED(5);
  right_fwd = new DCMotor(1,FORWARD);
  right_bwd = new DCMotor(1,BACKWARD);
  left_fwd = new DCMotor(2, FORWARD);
  left_bwd = new DCMotor(2, BACKWARD);
  pulley_up = new DCMotor(3, FORWARD);
  pulley_down = new DCMotor(3, BACKWARD);
  pusher_out = new DCMotor(4, FORWARD);
  pusher_in = new DCMotor(4, BACKWARD);
  selector_servo = new IDP_servo(9); // pin 9
  hall_effect1 = new Button(2); // pin 2
  hall_effect2 = new Button(3);
  IR_sensor = new Button(4);
  hall_led = new LED(8);
  IR_led = new LED(6);
  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
// initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  input_command.reserve(200);

  establishContact();   //send a byte to establish contact until receiver responds
}

void loop() {
	if ((hall_effect1 -> read_state())||(hall_effect2 -> read_state())){
		hall_led -> set_state(HIGH);
	}else{
		hall_led -> set_state(LOW);
	}
	if (IR_sensor -> read_state()){ //IR sensor is inverted
		IR_led -> set_state(HIGH);
	}else{
		IR_led -> set_state(LOW);
	}
    if (string_complete) {
    	switch(input_command[0]){
    	case 'a':
    		right_fwd->set_state(int(input_command[1])); //  reverts Char input back into int
			break;
    	case 'b':
			right_bwd->set_state(int(input_command[1]));
			break;
    	case 'c':
			left_fwd->set_state(int(input_command[1]));
			break;
    	case 'd':
			left_bwd->set_state(int(input_command[1]));
    	    break;
    	case 'e':
			selector_servo->set_state(int(input_command[1])); //position arg
			break;
    	case 'f':
			pulley_up->set_state(int(input_command[1]));
			break;
    	case 'g':
			pulley_down->set_state(int(input_command[1]));
			break;
    	case 'h':
			pusher_out->set_state(int(input_command[1]));
			break;
		case 'i':
			pusher_in->set_state(int(input_command[1]));
			break;
		case 'j':
			Serial.write((hall_effect1 -> read_state())||(hall_effect2 -> read_state()));
			break;
		case 'k':
			Serial.write(IR_sensor -> read_state());
			break;
		case 'l':
			drive_led -> set_state(int(input_command[1]));

    	default :;
    	}
    // clear the string:
    input_command = "";
    string_complete = false;
  }

 }


void serialEvent() {
  //This is where commands come in
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the input_command, 1st should be a Char, second an int Char conversion just to make it fit in string
    input_command += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      string_complete = true;
    }
  }
}





void establishContact() {
    // written mostly get familiar with

    //THIS FUNC IN SETUP, "handshake" in python immediately after port connection established
    Serial.write("hello"); // send handshake message
    int counter = 0;
    // loops until it gets something or it times out
    while(true){

    if (Serial.available() > 0){
      int message = Serial.read();
      Serial.write(char(message)); // should receive an H
      break;
    }else if(counter == 20){
      for( int a = 0; a < 10; a++ ){
       digitalWrite(LED_BUILTIN, HIGH);
       delay(100); //flashing LED indicates failed connection
       digitalWrite(LED_BUILTIN, LOW);
       delay(100);
       }
       break;
    }else{
      counter++;
      delay(500);
    }

    }
}


