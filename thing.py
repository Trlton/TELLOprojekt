import serial
import tkinter as tk
from tkinter import ttk

# Establish serial connection to Arduino
arduino = serial.Serial('COM9', 9600)  # Replace '/dev/ttyACM0' with your Arduino's port

# Create GUI window
root = tk.Tk()
root.title("Drone Controller")
root.geometry("400x300")

# Create GUI elements
thumbstick_label = ttk.Label(root, text="Thumbstick Control")
thumbstick_label.grid(row=0, column=0, padx=10, pady=10)

x_axis_label = ttk.Label(root, text="X-Axis:")
x_axis_label.grid(row=1, column=0, padx=10, pady=5)

y_axis_label = ttk.Label(root, text="Y-Axis:")
y_axis_label.grid(row=2, column=0, padx=10, pady=5)

x_axis_value_label = ttk.Label(root, text="0")
x_axis_value_label.grid(row=1, column=1, padx=10, pady=5)

y_axis_value_label = ttk.Label(root, text="0")
y_axis_value_label.grid(row=2, column=1, padx=10, pady=5)

thumbstick_indicator = ttk.Label(root, text="Thumbstick Position:", font=("Arial", 12, "bold"))
thumbstick_indicator.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Define update function
def update_thumbstick_position():
    data = arduino.readline().decode().strip()  # Read data from Arduino
    x_axis, y_axis = data.split(",")  # Parse data

    # Update labels
    x_axis_value_label.config(text=x_axis)
    y_axis_value_label.config(text=y_axis)

    # Update thumbstick position indicator
    thumbstick_position = f"X: {x_axis}, Y: {y_axis}"
    thumbstick_indicator.config(text=thumbstick_position)

    # Send data to drone (replace with your drone control logic)
    # Example:
    # arduino.write(f"{x_axis},{y_axis}\n".encode())

    # Schedule next update
    root.after(100, update_thumbstick_position)

# Start update loop
update_thumbstick_position()

# Run the GUI
root.mainloop()