import sys
import serial
import time
import pygame

class Ui:
    def __init__(self, com_port):
        self.init_window()
        self.init_serial_communication(com_port)
        self.init_variables()
        self.init_fonts()

    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Arduino Data Visualization")

    def init_serial_communication(self, com_port):
        try:
            global ser
            ser = serial.Serial(com_port, 9600)
            print(f"Connected to Arduino on port {com_port}")
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            sys.exit(1)

    def init_variables(self):
        self.ax = self.ay = self.az = 0
        self.gx = self.gy = self.gz = 0
        self.temp = 0
        self.last_keypad_input = "None"

        self.keypad_button_positions = [
            (100, 100),
            (200, 100),
            (300, 100),
            (400, 100),
            (100, 200),
            (200, 200),
            (300, 200),
            (400, 200),
            (100, 300),
            (200, 300),
            (300, 300),
            (400, 300)
        ]

        self.keypad_button_colors = [
            (0, 0, 255),
            (0, 255, 0),
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
            (128, 128, 128),
            (255, 255, 255),
            (128, 0, 0),
            (0, 128, 0),
            (0, 0, 128),
            (128, 128, 0)
        ]

    def init_fonts(self):
        self.font = pygame.font.Font(None, 24)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update_data()
            self.draw_ui()

            pygame.display.flip()

    def update_data(self):
        data = get_sensor_data()
        if data:
            self.ax, self.ay, self.az, self.gx, self.gy, self.gz, self.temp = data

            # Get keypad data and extract the key number
            keypad_data = get_keypad_data_from_serial()
            if keypad_data:
                self.last_keypad_input = keypad_data[0]  # Assuming the first character is the key number

    def draw_ui(self):
        self.screen.fill((230, 230, 230))  # Light gray background

        # Draw keypad buttons
        for i, (x, y) in enumerate(self.keypad_button_positions):
            pygame.draw.rect(self.screen, self.keypad_button_colors[i], (x, y, 100, 50))
            text_surface = self.font.render(str(i), True, (255, 255, 255))  # Display key numbers
            self.screen.blit(text_surface, (x + 35, y + 15))

        # Draw sensor data
        draw_sensor_data_box(self.screen, 500, 50, 250, 200, "Accelerometer", (self.ax, self.ay, self.az))
        draw_sensor_data_box(self.screen, 500, 270, 250, 200, "Gyroscope", (self.gx, self.gy, self.gz))
        draw_sensor_data_box(self.screen, 500, 490, 250, 50, "Temperature", (self.temp,))

        # Draw keypad input label
        keypad_label_text = f"Last Keypad Input: {self.last_keypad_input}"
        keypad_label_surface = self.font.render(keypad_label_text, True, (0, 0, 0))
        self.screen.blit(keypad_label_surface, (50, 50))


def draw_sensor_data_box(screen, x, y, width, height, data_label, data_values):
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)  # Draw box with border
    text_surface = self.font.render(data_label, True, (30, 30, 30))
    screen.blit(text_surface, (x + 10, y + 5))  # Label with padding

    # Display individual data values
    for i, value in enumerate(data_values):
        value_text = f"{value:.2f}"  # Format to 2 decimal places
        value_surface = self.font.render(value_text, True, (30, 30, 30))
        screen.blit(value_surface, (x + 50 + i * 80, y + 25))  # Aligned values with padding


def get_keypad_data_from_serial():
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("Keypad Data:"):
            return line.split(":")[1]
        return None
    except:
        print("Error reading keypad data")
        return None


if __name__ == "__main__":
    main()
