import pafy
import requests

from subprocess import Popen, PIPE

API_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"
API_KEY = "AIzaSyB-LEesjGOVHPCbClNLgk1ubrXAYTYA8tU"

PARAMS = {
  "key": API_KEY,
  "part": "snippet",
  "maxResults": 1,
  "order": "relevance",
  "type": "video",
  "fields":"items(id/videoId,snippet/title)"
}

mplayer = None

def play_from_search(query):
  global mplayer

  stop()
  url, title = _get_video_from_search(query)

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

def _get_video_from_search(query):
  payload = dict(PARAMS)
  payload["q"] = query
  r = requests.get(API_ENDPOINT, params=payload)
  video = r.json()["items"][0]
  url = video["id"]["videoId"]
  name = video["snippet"]["title"]
  return (url, name)