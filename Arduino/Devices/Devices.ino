#include "Arduino.h"
//The setup function is called once at startup of the sketch
int sensorPin = A0;    // select the input pin for the potentiometer


void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  //Serial.println(sensorValue);
  float voltage = map(sensorValue, 0, 1024, 0.0, 500.0)/100.0; // Divide by 1024 * 5V to get into 1-5 range
  Serial.println(voltage);
}
