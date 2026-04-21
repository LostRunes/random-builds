#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  String uid = "";

for (byte i = 0; i < mfrc522.uid.size; i++) {
  if (mfrc522.uid.uidByte[i] < 0x10) {
    uid += "0";  // add leading zero
  }
  uid += String(mfrc522.uid.uidByte[i], HEX);
  if (i != mfrc522.uid.size - 1) uid += " ";
}

uid.toUpperCase();
Serial.println(uid);  // send to PC
  delay(1000);
}