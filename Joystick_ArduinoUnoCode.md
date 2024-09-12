Arduino reader til analog port A0 (Til joystick
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
Python kode til analog port reader A0
Python code to read data from Arduino
import serial
import time

Configure the serial port to which Arduino is connected
arduino_port = 'COM8'
baud_rate = 9600

Open the serial port connection
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

Give the Arduino some time to initialize
time.sleep(2)

try:
    while True:
        # Read a line from the serial port
        data = ser.readline().decode('utf-8').strip()

        if data:
            print(f'Joystick Value: {data}')

        # Small delay for reading stability
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    # Close the serial connection when done
    ser.close()
