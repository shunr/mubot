from music import music_player
import speech_recognition as sr

def _parse_nlp(result):
    query = None
    print(result)
    entities = result.split()
    command = entities[0].lower().strip('.')
    if command == "play" and len(entities) <= 1:
        return None
    if command == "play":
      query = " ".join(entities[1:]).lower()
    return (command, query)

"""
def _parse_nlp(result):
    query = None
    print(result)
    entities = result["entities"]
    if "command" not in entities:
        return None
    command = result["entities"]["command"][0]["value"]
    if command == "play" and "search_query" not in entities:
        return None
    if command == "play":
      query = result["entities"]["search_query"][0]["value"]
    return (command, query)
"""

def _recognize(recognizer, audio):
    print("ok")
    try:
        result = recognizer.recognize_bing(audio, "b9bfada8b4ab42a480fe18b7c3f53911")
        #result = recognizer.recognize_sphinx(audio)
        #result = recognizer.recognize_houndify(audio, "HOd15CyEeEKoEE8qErKGrw==", "95gCvx1wB8xrUHWyxG7xd0ajsQB-T7jH5Kowo7q6O3XGUelbZGX2XPLoVyHLVR7ILVoL82r_q-YOlwzgbY2Vpg==")
        command = _parse_nlp(result)
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None


def start(callback):
    r = sr.Recognizer()
    m = sr.Microphone()
    r.pause_threshold = 0.8
    r.dynamic_energy_adjustment_ratio = 2
    with m as source:
        r.adjust_for_ambient_noise(source)
        phrase = r.listen(source, phrase_time_limit=3.5)
        callback(_recognize(r, phrase))

    
