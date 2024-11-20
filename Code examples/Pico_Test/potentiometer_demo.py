from machine import Pin, ADC  # Import ADC module
import time

gp0 = ADC(0)  # Set gp0 to ADC input

print('Reading a potentiometer demo.')

while True:
    led.value(not led.value())
    gp0_value = gp0.read_u16()  # Read potentiometer value from gp0 pin
    print(f'gp0 value: {gp0_value}')
    time.sleep(0.05)
