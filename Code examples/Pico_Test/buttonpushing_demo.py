from machine import Pin
import time

# Define the pin connected to the button
button_pin = Pin(0, Pin.IN, Pin.PULL_UP)

while True:
    if button_pin.value() == 0:
        print('Button pressed')
    else:
        print('Button released')
    print(button_pin.value())
    time.sleep(0.5)
    
    