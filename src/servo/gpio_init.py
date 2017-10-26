import RPi.GPIO as GPIO
import meme 

FREQUENCY = 50 #50Hz seems to be a good value but there is room for experimenting
PINS_USED = (3, 5, 7, 8, 10)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PINS_USED, GPIO.OUT)

SERVOS = [GPIO.PWM(pin, FREQUENCY) for pin in PINS_USED]
for servo in SERVOS:
    servo.start(0) #Default duty cycle is 0.0

#Do shit
meme.move_servo(SERVOS[0], 12, 2)

for servo in SERVOS:
    servo.stop()

GPIO.cleanup()


