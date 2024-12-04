from machine import Pin, ADC
import time

# Define the pin connected to the button
button_pin = Pin(1, Pin.IN, Pin.PULL_UP)
GP11_pin = Pin(16, Pin.OUT)
potentiometer = ADC(Pin(26))

# Switch to check whether button is currently held down
buttonState = button_pin.value()

# Potentiometer reading to switch off
potCutOff = 51000
#46000
#55000

while True:
    if button_pin.value() == 0 and buttonState == 1:
        print('Button pressed')
        
        buttonState = 0
        
    if button_pin.value() == 1 and buttonState == 0:
        print('Button released')
        buttonState = 1
        
    pot_value = potentiometer.read_u16()  # Read the ADC value (0-65535)
    print(pot_value)
    
    if buttonState == 0 and pot_value > potCutOff:
        GP11_pin.value(1)
    else:
        GP11_pin.value(0)
        
    # time.sleep(0.05)  # Delay for 100ms
    