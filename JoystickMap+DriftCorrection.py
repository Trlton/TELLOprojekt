import serial
from djitellopy import tello
import time

drone = tello.Tello()


# Replace with your Arduino serial port
SERIAL_PORT = 'COM10'

BAUD_RATE = 9600

# Drift compensation value for Y-axis
DRIFT_COMPENSATION = 0


def map_value(value, from_min, from_max, to_min, to_max):
    return int((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)


def read_data_from_arduino():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                x_str, y_str = line.split(',')

                # Convert to integers
                x = int(x_str)
                y = int(y_str)

                # Apply drift compensation
                y_compensated = y - DRIFT_COMPENSATION

                # Map joystick values from 63-190 to desired range (e.g., -100 to 100)
                x_mapped = map_value(x, 258, 764, -100, 100)  # Example range -100 to 100
                y_mapped = int(2+(map_value(y, 258, 762, -102, 101)))  # Example range -100 to 100

                # Print mapped values or send to drone


                drone.send_rc_control(y_mapped,x_mapped,0,0)
                time.sleep(0.1)
if __name__ == "__main__":
    read_data_from_arduino()
