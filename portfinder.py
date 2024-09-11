import sys

import serial.tools.list_ports
import os

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description:
            return port.device
    return None

def main():
    # Handle command-line arguments if needed
    if len(sys.argv) > 1 and sys.argv[1] == "--get-port":
        arduino_port = find_arduino_port()
        if arduino_port:
            print(arduino_port)
        else:
            print("No Arduino found.")
    else:
        print("Usage: python portfinder.py --get-port")

if __name__ == "__main__":
    main()