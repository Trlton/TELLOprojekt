import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
from djitellopy import Tello

# Initialize the Tello drone
tello = Tello()

# Connect to the Tello drone
tello.connect()


# Function to automatically detect the Arduino port
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'CH340' in port.description:
            return port.device
    return None


# Find the Arduino port automatically
arduino_port = find_arduino_port()
if not arduino_port:
    raise Exception("Arduino not found! Please check the connection.")

# Initialize the serial connection with the detected port
ser = serial.Serial(arduino_port, 115200, timeout=1)

# Thresholds for joystick to prevent noise and define direction
JOYSTICK_CENTER_X = 509
JOYSTICK_CENTER_Y = 505
THRESHOLD = 60  # Sensitivity threshold around the center for no movement
is_flying = False  # Global variable to track drone state


# Process joystick data to move the drone
def process_joystick_data(x, y):
    global is_flying

    if y > 1000:  # Joystick is clicked down
        if not is_flying:
            tello.takeoff()  # Take off if not flying
            is_flying = True
        else:
            tello.land()  # Land if already flying
            is_flying = False

    elif x < (JOYSTICK_CENTER_X - THRESHOLD):  # Move left
        tello.move_left(20)
    elif x > (JOYSTICK_CENTER_X + THRESHOLD):  # Move right
        tello.move_right(20)

    if y < (JOYSTICK_CENTER_Y - THRESHOLD):  # Move forward
        tello.move_forward(20)
    elif y > (JOYSTICK_CENTER_Y + THRESHOLD) and y < 1000:  # Move backward
        tello.move_back(20)


# Function to process keypad data (numpad 2, 4, 6, 8, etc.)
def process_keypad_data(hex_data):
    # Mapping numpad keys to movements
    key_map = {
        '2': tello.move_forward,      # Numpad 2: Forward
        '4': tello.move_left,         # Numpad 4: Left
        '6': tello.move_right,        # Numpad 6: Right
        '8': tello.move_back,         # Numpad 8: Backward
        '1': lambda: tello.move_left(20) or tello.move_forward(20),  # Numpad 1: Left-Forwards
        '3': lambda: tello.move_right(20) or tello.move_forward(20),  # Numpad 3: Right-Forwards
        '7': lambda: tello.move_left(20) or tello.move_back(20),     # Numpad 7: Left-Backwards
        '9': lambda: tello.move_right(20) or tello.move_back(20),    # Numpad 9: Right-Backwards
        '5': tello.flip_forward,      # Numpad 5: Flip
        '*': lambda: tello.move_up(20),  # Numpad *: Move Up
        '#': lambda: tello.move_down(20)  # Numpad #: Move Down
    }

    # Call the appropriate movement function if the key exists in the map
    if hex_data in key_map:
        key_map[hex_data]()  # Execute the mapped function


# Function to update the GUI with joystick and keypad data
def update_data():
    try:
        line = ser.readline().decode('utf-8').strip()  # Read a line from serial
        if line.startswith("Keypad Data:"):
            hex_data = line.split(":")[1].strip()  # Extract hex data
            keypad_data.set(f"Keypad: {hex_data}")
            process_keypad_data(hex_data)  # Process the numpad key inputs
        elif "X,Y" in line:  # Expecting joystick data format: "The X and Y coordinate is: 509,505"
            xy_data = line.split(":")[1].strip()
            x_value, y_value = map(int, xy_data.split(","))
            joystick_data.set(f"Joystick: {x_value}, {y_value}")
            process_joystick_data(x_value, y_value)  # Control drone using joystick
    except Exception as e:
        print(f"Error: {e}")

    root.after(100, update_data)  # Schedule the function to run every 100ms


# GUI Setup
root = tk.Tk()
root.title("Joystick and Keypad Control")
root.geometry("400x200")

# Labels for joystick and keypad data
ttk.Label(root, text="Joystick Data:").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(root, text="Keypad Data:").grid(column=0, row=1, padx=10, pady=10)

# Variables to store the data
joystick_data = tk.StringVar()
keypad_data = tk.StringVar()

# Dynamic labels to show real-time data
ttk.Label(root, textvariable=joystick_data).grid(column=1, row=0, padx=10, pady=10)
ttk.Label(root, textvariable=keypad_data).grid(column=1, row=1, padx=10, pady=10)

# Call the function to update data from serial
root.after(100, update_data)

# Start the GUI loop
root.mainloop()

# Close serial connection when done
ser.close()
