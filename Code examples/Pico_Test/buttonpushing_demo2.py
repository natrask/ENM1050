from machine import Pin
import time

# Define the pin connected to the button
button_pin = Pin(0, Pin.IN, Pin.PULL_UP)


buttonState = button_pin.value()

while True:
    if button_pin.value() == 0 and buttonState == 1:
        print('Button pressed')
        buttonState = 0
    if button_pin.value() == 1 and buttonState == 0:
        print('Button released')
        buttonState = 1
