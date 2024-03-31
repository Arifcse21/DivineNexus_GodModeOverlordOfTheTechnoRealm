import machine
import time

# Define GPIO pin for the built-in LED (may vary)
led_pin = 2

# Initialize built-in LED pin
led = machine.Pin(led_pin, machine.Pin.OUT)

