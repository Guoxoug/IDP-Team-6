// using serialEvent(), called at the end of each loop (called when data is available)
// run motor for a bit
#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *myMotor = AFMS.getMotor(1);
// You can also make another motor on port M2
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

void establishContact();
String input_command = "";         // a String to hold incoming data
bool string_complete = false;  // whether the string is complete

void setup() {
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)

  
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
    case 'f' : 
    //guys_motor_function(int(input_command[1]));
    //digitalWrite(LED_BUILTIN, HIGH);
    basic_motor(50);
    
    break;
    case 'b' :
    //digitalWrite(LED_BUILTIN, LOW); 
  //guys_other_motor_function(int(input_command[1]));
    basic_motor(0);
    break;
    
    default :;
 }
    // clear the string:
    input_command = "";
    string_complete = false;
  }

 }


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the input_command:
    input_command += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      string_complete = true;
    }
  }
}


  


void establishContact() {
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

void basic_motor(int power){
 myMotor->setSpeed(power);
  myMotor->run(FORWARD);
  // turn on motor
  myMotor->run(RELEASE); 
  myMotor->run(FORWARD);
}
