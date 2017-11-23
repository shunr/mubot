import pigpio
import time

# pigpio uses BCM pin numbers
RED = 17
GREEN = 27
BLUE = 22
PINS_USED = [RED, GREEN, BLUE]
PI = pigpio.pi()
PWM_RANGE = (750, 2500)

'''
The selected pulsewidth will continue to be transmitted until changed by a subsequent
call to set_servo_pulsewidth.
The pulsewidths supported by servos varies and should probably be determined by experiment.
A value of 1500 should always be safe and represents the mid-point of rotation.
'''


class LEDController(object):
    def __init__(self):
        for pin in PINS_USED:
            PI.set_mode(LED_PIN, pigpio.OUTPUT)
            PI.set_PWM_frequency(pin, 100)
            time.sleep(1)
        print("Initialized GPIO")

    def change_brightness_r(self, intensity):
        PI.set_PWM_dutycycle(RED,intensity)
        time.sleep(0.1)
    
    def change_brightness_g(self, intensity):
        PI.set_PWM_dutycycle(GREEN,intensity)
        time.sleep(0.1)

    def change_brightness_b(self, intensity):
        PI.set_PWM_dutycycle(BLUE,intensity)
        time.sleep(0.1)

    def cleanup(self):
        for pin in PINS_USED:
            PI.set_mode(pin, pigpio.INPUT)
        PI.stop()
