import pafy
from subprocess import Popen, PIPE
from bot import youtube

mplayer = None

def play_from_search(query):
  global mplayer

  stop()
  url, title = youtube.get_video_from_search(query)

  video = pafy.new(url)
  audio_streams = video.audiostreams
  best_audio = video.getbestaudio(preftype="webm")
  print("Playing" + title, best_audio.get_filesize())

  filename = best_audio.download("./tracks/track")

  mplayer = Popen(["mplayer", "-slave", "-quiet", filename], stdin=PIPE, stdout=PIPE)

def stop():
  global mplayer
  if mplayer != None:
    mplayer.kill()
  mplayer = None
