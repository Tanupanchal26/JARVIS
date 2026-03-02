import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import config
import musicLibrary
from openai import OpenAI

recognizer = sr.Recognizer()
tts = pyttsx3.init()

# Configure TTS settings
tts.setProperty('rate', config.TTS_RATE)
tts.setProperty('volume', config.TTS_VOLUME)

def speak(text):
    tts.say(text)
    tts.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country={config.NEWS_COUNTRY}&apiKey={config.NEWS_API_KEY}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                speak("Here are the top news headlines")
                for i, article in enumerate(articles[:config.NEWS_HEADLINES_COUNT]):
                    speak(f"News {i+1}: {article['title']}")
            else:
                speak("No news found")
        else:
            speak("Unable to fetch news")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=config.TIMEOUT, phrase_time_limit=config.PHRASE_TIME_LIMIT)
            word = r.recognize_google(audio)
            if word.lower() == config.WAKE_WORD:
                speak("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
