import speech_recognition as sr
import webbrowser
import time
import os
import requests
from gtts import gTTS
import pygame
import music_library
import google.generativeai as genai
import threading
from client import ask_llm
from dotenv import load_dotenv

load_dotenv()

running = False
assistant_thread = None

recognizer = sr.Recognizer()
pygame.mixer.init()

NEWS_API_KEY=os.getenv("NEWS_API_KEY")

# ----------------SPEAK----------------
def speak(text):
    def run_speech():
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove("temp.mp3")

    threading.Thread(target=run_speech).start()
# ----------------COMMANDS----------------
def processCommand(c):
    print("MUKESH :- ",c)
    c = c.lower()

    if "open youtube" in c:
        print("Openinng Youtube...")
        speak("Openinng Youtube...")
        webbrowser.open("https://youtube.com")

    elif "open google" in c:
        print("Openinng Google...")
        speak("Openinng Google...")
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        print("Openinng facebook...")
        speak("Openinng facebook...")
        webbrowser.open("https://facebook.com")

    elif "open instagram" in c:
        print("Openinng instagram...")
        speak("Openinng instagram...")
        webbrowser.open("https://instagram.com")

    elif "open github" in c:
        print("Openinng Github...")
        speak("Openinng Github...")
        webbrowser.open("https://github.com")

    elif "open notepad" in c:
        print("Openinng Notepad...")
        speak("Openinng Notepad...")
        os.system("notepad")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        link = music_library.music.get(song)
        if link:
            speak("Playing...")
            webbrowser.open(link)
        else:
            speak("Song not found")

    elif "news" in c:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        )
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            speak("Here are the top news headlines:- ")
            for article in articles[:5]:
                print(article["title"])
                speak(article["title"])
                time.sleep(4)
        else:
            speak("Unable to fetch news")

    else:
        reply = ask_llm(c)
        print("PHANTOM :- ",reply)
        speak(reply)

# ----------------MAIN LOOP----------------
def phantom_loop():
    global running
    print("Initializing Phantom.....")
    speak("Initializing Phantom.....")

    while running:
        try:
            print("Waiting for wake word....")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            try:
                wake_word = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                continue  
            except sr.RequestError:
                print("API unavailable")
                continue

            if wake_word.lower() == "phantom":
                speak("Yes....Listening!!")
                print("Yes....Listening!!")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                try:
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
                except sr.UnknownValueError:
                    continue 
                except sr.RequestError:
                    speak("Network issue")

        except Exception as e:
            print("Error:", e)


