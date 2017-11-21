import RPi.GPIO as GPIO
import time

FREQUENCY = 50  # 50Hz seems to be a good value but there is room for experimenting
SERVO_ARM = 3
SERVOS = {}
PINS_USED = [SERVO_ARM]

DUTY_CYCLE_RANGE = (3, 14)


class ServoController(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PINS_USED, GPIO.OUT)

        for pin in PINS_USED:
            SERVOS[pin] = GPIO.PWM(pin, FREQUENCY)
            SERVOS[pin].start(0)  # Default duty cycle is 0.0
        print("Initialized GPIO")

    def move_arm(self, angle):
        _move_servo(SERVO_ARM, _angle_to_duty_cycle(angle))

    def cleanup(self):
        for servo in SERVOS:
            SERVOS[servo].stop()
        GPIO.cleanup()


def _move_servo(servo, duty_cycle):
    if servo not in SERVOS:
        return
    SERVOS[servo].ChangeDutyCycle(duty_cycle)


def _angle_to_duty_cycle(angle):
    range = DUTY_CYCLE_RANGE[1] - DUTY_CYCLE_RANGE[0]
    return (DUTY_CYCLE_RANGE[0] + range * angle / 180)
