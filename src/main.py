import pafy
import sys
from subprocess import Popen, PIPE
import time
from music import speech_input
from music import music_player

def play(command):
    if command != None:
        if command[0] == "play":
            music_player.play_from_search(command[1])
        elif command[0] == "stop":
            music_player.stop()

while 1:
  #speech_input.start(play)
  c = input().split()
  a = (c[0], " ".join(c[1:]))
  play(a)
