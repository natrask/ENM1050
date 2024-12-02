from machine import ADC, Pin
import time

# Initialize ADC on pin 26 (for Raspberry Pi Pico)
potentiometer = ADC(Pin(26))

# Open the file in write mode
with open("potentiometer_values.txt", "w") as file:
    while True:
        pot_value = potentiometer.read_u16()  # Read the ADC value (0-65535)
        file.write(f"Potentiometer value: {pot_value}\n")
        file.flush()  # Ensure the value is written to the file immediately
        print("Potentiometer value:", pot_value)
        time.sleep(0.1)

        