const int joystickPinX = A0;  // X-axis of joystick
const int joystickPinY = A1;  // Y-axis of joystick

void setup() {
  Serial.begin(9600);  // start connection 
}

void loop() {   // Read axis values
  int joystickValueX = analogRead(joystickPinX);  
  int joystickValueY = analogRead(joystickPinY);  

  // Send joystick values over serial
  Serial.print(joystickValueX);
  Serial.print(",");
  Serial.println(joystickValueY);

  delay(100);  // Delay to optimize responestime on other side

}
