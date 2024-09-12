import serial

# Replace with your Arduino serial port
SERIAL_PORT = 'COM8'  # For Linux
# SERIAL_PORT = 'COM3'       # For Windows (example COM3)

BAUD_RATE = 9600

# Drift compensation value for Y-axis
DRIFT_COMPENSATION = 2  # Change this if necessary


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
                x_mapped = map_value(x, 63, 190, -100, 100)  # Example range -100 to 100
                y_mapped = map_value(max(min(y_compensated, 190), 63), 63, 190, -100, 100)  # Example range -100 to 100

                # Print mapped values or send to drone
                print(f"X: {x_mapped}, Y: {y_mapped}")


if __name__ == "__main__":
    read_data_from_arduino()
