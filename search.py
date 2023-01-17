import requests
import pyttsx3
 
engine = pyttsx3.init()
text = "How to learn ML"
result = requests.get(f"http://127.0.0.1:5001/chat?q={text}")
print(result.content)
engine.say(result.content.decode('utf-8'))
engine.runAndWait()