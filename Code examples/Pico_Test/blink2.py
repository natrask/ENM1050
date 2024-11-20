from machine import Pin
import time

led = Pin(0, Pin.OUT)
print('Blinking LED example')

while True:
    led.value(not led.value())
    time.sleep(0.5)
    