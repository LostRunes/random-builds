#include <SPI.h>
#include <XPT2046_Touchscreen.h>

#define CS_PIN 10
#define IRQ_PIN 2

XPT2046_Touchscreen ts(CS_PIN, IRQ_PIN);

void setup() {
  Serial.begin(9600);
  ts.begin();
  ts.setRotation(1);

  Serial.println("Touch test started...");
}

void loop() {
  if (ts.touched()) {
    TS_Point p = ts.getPoint();

    Serial.print("X: ");
    Serial.print(p.x);
    Serial.print(" | Y: ");
    Serial.println(p.y);

    delay(150);
  }
}