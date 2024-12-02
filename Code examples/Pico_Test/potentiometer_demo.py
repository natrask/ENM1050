from machine import ADC, Pin
import time

# Initialize ADC on pin 26 (for Raspberry Pi Pico)
potentiometer = ADC(Pin(26))

while True:
    pot_value = potentiometer.read_u16()  # Read the ADC value (0-65535)
    print("Potentiometer value:", pot_value)
    time.sleep(0.1)
    