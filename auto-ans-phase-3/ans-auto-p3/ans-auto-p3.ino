#include <Keyboard.h>

const int pinCapture = 2;
const int pinType = 3;
const int pinStop = 4;

bool t1 = false, t2 = false, t3 = false;

void setup() {
  pinMode(pinCapture, INPUT_PULLUP);
  pinMode(pinType, INPUT_PULLUP);
  pinMode(pinStop, INPUT_PULLUP);

  Keyboard.begin();
}

void loop() {

  // 🔵 Capture (Ctrl + Alt + C)
  if (digitalRead(pinCapture) == LOW && !t1) {
    t1 = true;
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_LEFT_ALT);
    Keyboard.press('c');
    delay(100);
    Keyboard.releaseAll();
    delay(400);
  }
  if (digitalRead(pinCapture) == HIGH) t1 = false;


  // 🟢 Type (Ctrl + Alt + T)
  if (digitalRead(pinType) == LOW && !t2) {
    t2 = true;
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_LEFT_ALT);
    Keyboard.press('t');
    delay(100);
    Keyboard.releaseAll();
    delay(400);
  }
  if (digitalRead(pinType) == HIGH) t2 = false;


  // 🔴 STOP (Ctrl + Alt + X)
  if (digitalRead(pinStop) == LOW && !t3) {
    t3 = true;
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_LEFT_ALT);
    Keyboard.press('x');
    delay(100);
    Keyboard.releaseAll();
    delay(400);
  }
  if (digitalRead(pinStop) == HIGH) t3 = false;
}