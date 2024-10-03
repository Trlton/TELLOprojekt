// Arduino code to read joystick and send data via serial
const int joystickPinX = A0;  // X-axis of joystick
const int joystickPinY = A1;  // Y-axis of joystick

void setup() {
  Serial.begin(9600);  // Start serial communication
}

void loop() {
  int joystickValueX = analogRead(joystickPinX);  // Read X-axis value
  int joystickValueY = analogRead(joystickPinY);  // Read Y-axis value

  // Send joystick values over serial (as comma-separated values)
  Serial.print(joystickValueX);
  Serial.print(",");
  Serial.println(joystickValueY);

  delay(100);  // Delay to avoid flooding serial port

}
