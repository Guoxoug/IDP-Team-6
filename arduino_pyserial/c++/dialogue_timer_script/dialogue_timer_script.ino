
void establishContact();
void setup() {
  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
// initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  establishContact();   //send a byte to establish contact until receiver responds
}

void loop() {
  int incoming_byte;
 if (Serial.available() > 0){
      incoming_byte = Serial.read();
 }
 switch(incoming_byte){
    case 0 : 
    digitalWrite(LED_BUILTIN, LOW);
    break;
    case 1 : 
    digitalWrite(LED_BUILTIN, HIGH);
    break;
    case 2 : 
    digitalWrite(LED_BUILTIN, LOW);
    break;
    default :;
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
