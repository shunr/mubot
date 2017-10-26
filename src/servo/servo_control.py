import time
import RPi.GPIO as GPIO

def move_servo(servo, duty_cycle, sleep):
    servo.changeDutyCycle(duty_cycle)
    time.sleep(sleep)
