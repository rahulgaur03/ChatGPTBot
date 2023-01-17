import requests
import pyttsx3
import speech_recognition as sr

listener = sr.Recognizer()
engine = pyttsx3.init()

while True:
    text = ""
    with sr.Microphone() as source:
        print('listening...')
        voice = listener.listen(source)
        text = listener.recognize_google(voice)
        print(text)

    result = requests.get(f"http://127.0.0.1:5001/chat?q={text}")
    print(result.content)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(result.content.decode('utf-8'))
    engine.runAndWait()