// using serialEvent(), called at the end of each loop (called when data is available)


#include "Arduino.h"
#include "DeviceControllers.h"
#include "Adafruit_MotorShield.h"
LED* led;
DCMotor* right_fwd;
DCMotor* right_bwd;
DCMotor* left_fwd;
DCMotor* left_bwd;


void establishContact();
String input_command = "";         // a String to hold incoming data
bool string_complete = false;  // whether the string is complete

void setup() {
	AFMS.begin();   // create with the default frequency 1.6KHz


  led = new LED(LED_BUILTIN); //these declarations must come after Serial
  //led->print_pin_state();
  right_fwd = new DCMotor(1,FORWARD);
  right_bwd = new DCMotor(1,BACKWARD);
  left_fwd = new DCMotor(2, FORWARD);
  left_bwd = new DCMotor(2, BACKWARD);
  //right_fwd->print_pin_state();
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


