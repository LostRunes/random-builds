#include <Keyboard.h>

const int touchPin = 2;

void setup() {
  pinMode(touchPin, INPUT_PULLUP);
  Keyboard.begin();
}

void loop() {
  if (digitalRead(touchPin) == LOW) {
    delay(200);

    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_LEFT_ALT);
    Keyboard.press('g');
    delay(100);
    Keyboard.releaseAll();

    delay(2000);
  }
}