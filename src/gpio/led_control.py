import pigpio
import time

# pigpio uses BCM pin numbers
RED = 17
GREEN = 27
BLUE = 22
PINS_USED = [RED, GREEN, BLUE]
PI = pigpio.pi()

class LEDController(object):
    def __init__(self):
        for pin in PINS_USED:
            PI.set_mode(pin, pigpio.OUTPUT)
            PI.set_PWM_frequency(pin, 100)
            time.sleep(1)
        print("Initialized GPIO")

    def change_brightness_r(self, intensity):
        PI.set_PWM_dutycycle(RED,intensity)
    
    def change_brightness_g(self, intensity):
        PI.set_PWM_dutycycle(GREEN,intensity)

    def change_brightness_b(self, intensity):
        PI.set_PWM_dutycycle(BLUE,intensity)

    def cleanup(self):
        for pin in PINS_USED:
            PI.set_mode(pin, pigpio.INPUT)
        PI.stop()
