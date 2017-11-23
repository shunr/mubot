import pigpio
import time

# LEDController is used to change the intensity of the red, green and blue LEDs on the robot.
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
        print("Initialized LED Controller")

    def set_r(self, intensity):
        PI.set_PWM_dutycycle(RED, intensity * 0.9)
    
    def set_g(self, intensity):
        PI.set_PWM_dutycycle(GREEN,intensity * 0.8)

    def set_b(self, intensity):
        PI.set_PWM_dutycycle(BLUE, intensity)

    def cleanup(self):
        for pin in PINS_USED:
            PI.set_mode(pin, pigpio.INPUT)
        PI.stop()
