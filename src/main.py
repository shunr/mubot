import sys
import random
from music import speech_input
from music import music_player

from gpio import servo_control

controller = servo_control.ServoController()


def callback(data):
    print("move arm", data)
    #controller.move_arm(random.randint(3, 14))


def execute(command):
    if command != None:
        print(command)
        if command[0] == "play":
            music_player.play_from_search(command[1], callback)
        elif command[0] == "stop":
            music_player.stop()
        elif command[0] == "servo":
            print(command)
            if len(command) == 2:
                controller.move_arm_l(float(command[1]))
                controller.move_arm_r(float(command[1]))
                controller.move_head(float(command[1]))
                controller.move_body(float(command[1]))
        elif command[0] == "cleanup":
            controller.cleanup()
            sys.exit(0)


while 1:
    # speech_input.start(play)
    c = input().split()
    a = (c[0], " ".join(c[1:]))
    execute(a)
