import requests

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

def get_video_from_search(query):
  payload = dict(PARAMS)
  payload["q"] = query
  r = requests.get(API_ENDPOINT, params=payload)
  video = r.json()["items"][0]
  url = video["id"]["videoId"]
  name = video["snippet"]["title"]
  return (url, name)
