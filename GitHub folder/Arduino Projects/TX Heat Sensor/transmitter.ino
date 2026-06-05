#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const int LED_PIN = 13;
const int input_heat = A1;  

RF24 radio(9, 10);
const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();

  pinMode(input_heat, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int heatValue = analogRead(input_heat);  

  if (heatValue > 512) {  
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
    Serial.println("Mainit!!!");  
  }
}