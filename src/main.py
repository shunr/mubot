import pafy
import sys
from subprocess import Popen, PIPE
import time
from music import speech_input
from music import music_player
from gpio import servo_control

servo_control.init()

def execute(command):
    if command != None:
        if command[0] == "play":
            music_player.play_from_search(command[1])
        elif command[0] == "stop":
            music_player.stop()
        elif command[0] == "servo":
            if len(command) == 2:
              servo_control.move_arm(int(command[1]))
        elif command[0] == "cleanup":
            servo_control.cleanup()

while 1:
  #speech_input.start(play)
  c = input().split()
  a = (c[0], " ".join(c[1:]))
  execute(a)
