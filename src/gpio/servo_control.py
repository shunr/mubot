import RPi.GPIO as GPIO
import time

FREQUENCY = 50  # 50Hz seems to be a good value but there is room for experimenting
SERVO_ARM = 3
SERVOS = {}
PINS_USED = [SERVO_ARM]
initialized = False

def init():
  global initialized
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PINS_USED, GPIO.OUT)

  for pin in PINS_USED:
      SERVOS[pin] = GPIO.PWM(pin, FREQUENCY)
      SERVOS[pin].start(0)  # Default duty cycle is 0.0
  initialized = True
  print("Initialized GPIO")

def _move_servo(servo, duty_cycle):
    global initialized
    print(initialized)
    if not initialized:
      return
    SERVOS[servo].ChangeDutyCycle(duty_cycle)
    print("wew")

def move_arm(duty_cycle):
  _move_servo(SERVO_ARM, duty_cycle)


def cleanup():
    global initialized
    if not initialized:
      return
    for servo in SERVOS:
      SERVOS[servo].stop()
    GPIO.cleanup()
    initialized = False


