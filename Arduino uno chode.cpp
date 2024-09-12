#include "Wire.h"          // For I2C communication with BMI088
#include "BMI088.h"        // Include the BMI088 library
#include "SoftwareSerial.h"  // For keypad communication (if using SoftwareSerial)

// Define pins for SoftwareSerial if needed
#define RX_PIN 2
#define TX_PIN 3
SoftwareSerial keypadSerial(RX_PIN, TX_PIN);  // Initialize SoftwareSerial for the keypad

float ax = 0, ay = 0, az = 0;
float gx = 0, gy = 0, gz = 0;
int16_t temp = 0;
BMI088 bmi088( BMI088_ACC_ADDRESS, BMI088_GYRO_ADDRESS );

void setup() {
    Serial.begin(115200);  // Serial monitor for debugging
    Wire.begin();        // Initialize I2C communication
    
    // Initialize keypad serial communication
    keypadSerial.begin(115200);
    Serial.println("Initializing...");

    // Initialize the BMI088 sensor
    if (bmi088.isConnection()) {
        bmi088.initialize();
        Serial.println("BMI088 is connected.");
    } else {
        Serial.println("BMI088 is not connected. Please check connections.");
        while (1); // Halt if sensor is not found
    }
}

void loop() {
    // Check keypad data and send to serial
    //printKeypadData();

    // Check sensor data and send to serial
    //printSensorData();

    // Check joystick data and send to seriel
    printJoystickData();

    delay(500);  // Delay for stability
}

void printJoystickData() {
    int sensorValueX = analogRead(A0);  // Read X-axis (Joystick connected to A0)
    int sensorValueY = analogRead(A1);  // Read Y-axis (Joystick connected to A1)

    Serial.print("Joystick X,Y: ");
    Serial.print(sensorValueX);   // Print X-axis value
    Serial.print(", ");
    Serial.println(sensorValueY); // Print Y-axis value
}

void printKeypadData() {
    while (keypadSerial.available()) {
        uint8_t data = keypadSerial.read();
        Serial.print("Keypad Data:");
        Serial.println(data,HEX);  // Print data as hexadecimal for debugging
    }
}

void printSensorData() {
    // Get accelerometer and gyroscope data from BMI088
    bmi088.getAcceleration(&ax, &ay, &az);
    bmi088.getGyroscope(&gx, &gy, &gz);

    // Print accelerometer data
    Serial.print("ACC: ");
    Serial.print(ax);
    Serial.print(", ");
    Serial.print(ay);
    Serial.print(", ");
    Serial.println(az);

    // Print gyroscope data
    Serial.print("GYRO: ");
    Serial.print(gx);
    Serial.print(", ");
    Serial.print(gy);
    Serial.print(", ");
    Serial.println(gz);
}
