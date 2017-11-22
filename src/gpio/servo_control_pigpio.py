import pigpio
import time

# pigpio uses BCM pin numbers
SERVO_ARM_L = 2
SERVO_ARM_R = 3
SERVO_HEAD = 4
SERVO_BODY = 14
PINS_USED = [SERVO_ARM_L, SERVO_ARM_R, SERVO_HEAD, SERVO_BODY]
PI = pigpio.pi()
PWM_RANGE = (1000, 2000)

'''
The selected pulsewidth will continue to be transmitted until changed by a subsequent
call to set_servo_pulsewidth.
The pulsewidths supported by servos varies and should probably be determined by experiment.
A value of 1500 should always be safe and represents the mid-point of rotation.
'''


class ServoController(object):
    def __init__(self):
        for pin in PINS_USED:
            # 0 (off), 500 (most CCW), 2500 (most CW)
            PI.set_servo_pulsewidth(pin, 0)
            time.sleep(1)
        print("Initialized GPIO")

    def move_arm_l(self, angle):
        _move_servo(SERVO_ARM_L, _angle_to_pulse_width(angle))

    def move_arm_r(self, angle):
        _move_servo(SERVO_ARM_R, _angle_to_pulse_width(angle))

    def move_body(self, angle):
        _move_servo(SERVO_BODY, _angle_to_pulse_width(angle))

    def move_head(self, angle):
        _move_servo(SERVO_HEAD, _angle_to_pulse_width(angle))

    def cleanup(self):
        for pin in PINS_USED:
            PI.set_mode(pin, pigpio.INPUT)
        PI.stop()


def _move_servo(servo, pulse_width):
    if servo not in PINS_USED:
        return
    PI.set_servo_pulsewidth(servo, pulse_width)


def _angle_to_pulse_width(angle):
    pw_range = PWM_RANGE[1] - PWM_RANGE[0]
    return (PWM_RANGE[0] + pw_range * angle / 180)
