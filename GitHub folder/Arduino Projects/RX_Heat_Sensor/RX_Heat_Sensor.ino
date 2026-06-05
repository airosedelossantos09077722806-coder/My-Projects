#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const int LED_PIN = 13;

RF24 radio(9, 10);
const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();

  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (radio.available()) {
    char message[32] = "";
    radio.read(&message, sizeof(message));

    Serial.print("Received: ");
    Serial.println(message);

    if (strcmp(message, "Warning: Hot!") == 0) {
      Serial.println("ALERT: Heat detected from transmitter!");
      for (int i = 0; i < 5; i++) {
        digitalWrite(LED_PIN, HIGH);
        delay(200);
        digitalWrite(LED_PIN, LOW);
        delay(200);
      }
    }
  }
}