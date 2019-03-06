//// using serialEvent(), called at the end of each loop (called when data is available)
//// run motor for a bit
//
//#include <Wire.h>
//#include <Adafruit_MotorShield.h>
//#include "DeviceControllers.h"
//
////// Create the motor shield object with the default I2C address
////Adafruit_MotorShield AFMS = Adafruit_MotorShield();
////// Or, create it with a different I2C address (say for stacking)
////// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61);
////
////// Select which 'port' M1, M2, M3 or M4. In this case, M1
////Adafruit_DCMotor *right_motor = AFMS.getMotor(1);
////// You can also make another motor on port M2
////Adafruit_DCMotor *left_motor = AFMS.getMotor(2);
//
//DCMotor *right_fwd = new DCMotor(1, FORWARD);
//
//void establishContact();
//String input_command = "";         // a String to hold incoming data
//bool string_complete = false;  // whether the string is complete
//
//void setup() {
//  AFMS.begin();  // create with the default frequency 1.6KHz
//  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
//
//  // Set the speed to start, from 0 (off) to 255 (max speed)
//
//
//  // start serial port at 9600 bps:
//  Serial.begin(9600);
//  while (!Serial) {
//    ; // wait for serial port to connect. Needed for native USB port only
//  }
//// Initialise digital pin LED_BUILTIN as an output.
//  pinMode(LED_BUILTIN, OUTPUT);
//  input_command.reserve(200);
//
//  establishContact();   //send a byte to establish contact until receiver responds
//}
//
//void loop() {
//    if (string_complete) {
//    //Serial.print(input_command + 'g');
//   switch(input_command[0]){
//    case 'a' :
//
//      //guys_motor_function(int(input_command[1]));
//      //digitalWrite(LED_BUILTIN, HIGH);
//      right_motor_forward(int(input_command[1]-'0')*255/7);
//      /* IMPORTANT Char type in c++ is just an integer, so to get the integer value do char - '0'
//       *  Also be careful with integer calculations, remember that division is floored
//       */
//      Serial.print(int(input_command[1]-'0')*255/7);
//
//      break;
//    case 'b' :
//      //digitalWrite(LED_BUILTIN, LOW);
//      //guys_other_motor_function(int(input_command[1]));
//
//      right_motor_backward(int(input_command[1]-'0')*255/7);
//      break;
//    case 'c' :
//      //guys_motor_function(int(input_command[1]));
//      //digitalWrite(LED_BUILTIN, HIGH);
//       left_motor_forward(int(input_command[1]-'0')*255/7);
//       Serial.print(int(input_command[1]-'0')*255/7);
//
//      break;
//    case 'd' :
//    //digitalWrite(LED_BUILTIN, LOW);
//	//guys_other_motor_function(int(input_command[1]));
//
//     left_motor_backward(int(input_command[1]-'0')*255/7);
//    break;
//
//    default :;
//   }
//    // clear the string:
//    input_command = "";
//    string_complete = false;
//  }
//
// }
//
//
//void serialEvent() {
//  //This is where commands come in
//  while (Serial.available()) {
//    // get the new byte:
//    char inChar = (char)Serial.read();
//    // add it to the input_command:
//    input_command += inChar;
//    // if the incoming character is a newline, set a flag so the main loop can
//    // do something about it:
//    if (inChar == '\n') {
//      string_complete = true;
//    }
//  }
//}
//
//
//
//
//
//void establishContact() {
//    // written mostly get familiar with
//
//    //THIS FUNC IN SETUP, "handshake" in python immediately after port connection established
//    Serial.write("hello"); // send handshake message
//    int counter = 0;
//    // loops until it gets something or it times out
//    while(true){
//
//    if (Serial.available() > 0){
//      int message = Serial.read();
//      Serial.write(char(message)); // should receive an H
//      break;
//    }else if(counter == 20){
//      for( int a = 0; a < 10; a++ ){
//       digitalWrite(LED_BUILTIN, HIGH);
//       delay(100); //flashing LED indicates failed connection
//       digitalWrite(LED_BUILTIN, LOW);
//       delay(100);
//       }
//       break;
//    }else{
//      counter++;
//      delay(500);
//    }
//
//    }
//}
//
//void right_motor_forward(int power){
// right_motor->setSpeed(power);
//  right_motor->run(FORWARD);
//  // turn on motor
//  right_motor->run(RELEASE);
//  right_motor->run(FORWARD);
//}
//void right_motor_backward(int power){
// right_motor->setSpeed(power);
//  right_motor->run(BACKWARD);
//  // turn on motor
//  right_motor->run(RELEASE);
//  right_motor->run(BACKWARD);
//}
//void left_motor_forward(int power){
// left_motor->setSpeed(power);
//  left_motor->run(FORWARD);
//  // turn on motor
//  left_motor->run(RELEASE);
//  left_motor->run(FORWARD);
//}
//void left_motor_backward(int power){
// left_motor->setSpeed(power);
//  left_motor->run(BACKWARD);
//  // turn on motor
//  left_motor->run(RELEASE);
//  left_motor->run(BACKWARD);
//}
