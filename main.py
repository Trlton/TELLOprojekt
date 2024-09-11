import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk


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
ser = serial.Serial(arduino_port, 9600, timeout=1)

# Keypad mapping from hex values to actual buttons
keypad_mapping = {
    0xE1: '1',
    0xE2: '2',
    0xE3: '3',
    0xE4: '4',
    0xE5: '5',
    0xE6: '6',
    0xE7: '7',
    0xE8: '8',
    0xE9: '9',
    0xEA: '*',
    0xEB: '0',
    0xEC: '#'
}


# Function to update the GUI with sensor data
def update_data():
    try:
        line = ser.readline().decode('utf-8').strip()  # Read a line from serial
        if line.startswith("ACC:"):
            acc_data.set(line.split(":")[1].strip())
        elif line.startswith("GYRO:"):
            gyro_data.set(line.split(":")[1].strip())
        elif line.startswith("Keypad Data:"):
            hex_data = line.split(":")[1].strip()
            hex_value = int(hex_data, 16)  # Convert the hex string to an integer
            key = keypad_mapping.get(hex_value, "Unknown")  # Get the corresponding key or "Unknown"
            keypad_data.set(f"Pressed: {key}")
    except Exception as e:
        print(f"Error: {e}")

    root.after(100, update_data)  # Schedule the function to run every 100ms


# GUI Setup
root = tk.Tk()
root.title("Arduino Sensor Data")
root.geometry("400x200")

# Labels for Accelerometer, Gyroscope, and Keypad data
ttk.Label(root, text="Accelerometer Data:").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(root, text="Gyroscope Data:").grid(column=0, row=1, padx=10, pady=10)
ttk.Label(root, text="Keypad Data:").grid(column=0, row=2, padx=10, pady=10)

# Variables to store the data
acc_data = tk.StringVar()
gyro_data = tk.StringVar()
keypad_data = tk.StringVar()

# Dynamic labels to show real-time data
ttk.Label(root, textvariable=acc_data).grid(column=1, row=0, padx=10, pady=10)
ttk.Label(root, textvariable=gyro_data).grid(column=1, row=1, padx=10, pady=10)
ttk.Label(root, textvariable=keypad_data).grid(column=1, row=2, padx=10, pady=10)

# Call the function to update data from serial
root.after(100, update_data)

# Start the GUI loop
root.mainloop()

# Close serial connection when done
ser.close()
