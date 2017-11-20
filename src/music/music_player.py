import pafy
import requests
import wave
import pyaudio
import time

from music import analyzer

API_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"
API_KEY = "AIzaSyB-LEesjGOVHPCbClNLgk1ubrXAYTYA8tU"
FILETYPE = "m4a"
PARAMS = {
    "key": API_KEY,
    "part": "snippet",
    "maxResults": 1,
    "order": "relevance",
    "type": "video",
    "fields": "items(id/videoId,snippet/title)"
}


def play_from_search(query, callback):
    url, title = _get_video_from_search(query)

    video = pafy.new(url)
    audio_streams = video.audiostreams
    best_audio = video.getbestaudio(preftype=FILETYPE)
    print("Playing " + title, best_audio.get_filesize())
    t1 = time.time()
    filename = best_audio.download("./tracks/track." + FILETYPE)
    t2 = time.time()
    print("Time taken to download: {0:.6f}".format(t2-t1))

    t1 = time.time()
    transcoded = analyzer.transcode(filename)
    t2 = time.time()
    print("Time taken to transcode: {0:.6f}".format(t2-t1))
    _play(transcoded, analyzer.analyze(transcoded), callback)


def _play(filename, peaks, callback):
    CHUNK_SIZE = 1024

    # open a wav format music
    f = wave.open(filename, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    ind = 0
    data = f.readframes(CHUNK_SIZE)
    while data:
        if (peaks[ind] <= 0):
            a = 0
        elif (ind < 3 or (peaks[ind - 1] <= 0 and peaks[ind - 2] <= 0 and peaks[ind - 3] <= 0)):
            callback(peaks[ind])
        stream.write(data)
        ind += 1
        data = f.readframes(CHUNK_SIZE)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


def _get_video_from_search(query):
    payload = dict(PARAMS)
    payload["q"] = query
    r = requests.get(API_ENDPOINT, params=payload)
    video = r.json()["items"][0]
    url = video["id"]["videoId"]
    name = video["snippet"]["title"]
    return (url, name)
