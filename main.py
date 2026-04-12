# import speech_recognition as sr
# import webbrowser
# import pyttsx3
# import time
# import os
# import music_library
# import requests
# import google.generativeai as genai
# from gtts import gTTS
# import pygame

# recognizer = sr.Recognizer()
# engine = pyttsx3.init()

# def speak_old(text):
#     engine.say(text)
#     engine.runAndWait()
#     time.sleep(0.2)

# def speak(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')

#     # 1. Initialize mixer
#     pygame.mixer.init()

#     # 2. Load the MP3 file
#     pygame.mixer.music.load("temp.mp3") 

#     # 3. Play the music
#     pygame.mixer.music.play()

#     # 4. Keep the program running until the song ends
#     while pygame.mixer.music.get_busy():  # returns True while playing
#         pygame.time.Clock().tick(10)
#     pygame.mixer.music.unload() 
#     os.remove("temp.mp3")

 

#     completion = client.chat.completions.create(
#         model = "gpt-3.5-turbo",
#         messages=[
#             {"role":"system","content":"You are virtual assistant name"phantom skilled in general tasks like Alexa and Google Cloud. Give short responses"},
#             {"role":"user","content":command}

#         ]
#     )
#     return completion.choices[0].message.content

# def processCommand(c):
#     if "ope"phantom" in c.lower():
#         webbrowser.open("https:"phantom.com")
#     elif "open facebook" in c.lower():
#         webbrowser.open("https://facebook.com")
#     elif "open instagram" in c.lower():
#         webbrowser.open("https://instagram.com")
#     elif "open notepad" in c.lower():
#         os.system("notepad")
#     elif "open youtube" in c.lower():
#         webbrowser.open("https://youtube.com")
#     elif "open chrome" in c.lower():
#         webbrowser.open("https://chrome.com")
#     elif "open visual studio code" in c.lower():
#         os.system("visual studio code")
#     elif "open linkdin" in c.lower():
#         webbrowser.open("https://linkdin.com")
#     elif "open github" in c.lower():
#         webbrowser.open("https://github.com")
#     elif c.lower().startswith("play"):
#         song = c.lower().replace("play", "").strip()
#         link = music_library.music.get(song)
#         webbrowser.open(link)
#     elif "news" in c.lower():
#         r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2025-10-03&sortBy=publishedAt&apiKey={newsapi}")
#         if r.status_code == 200:
#             #Parse the JSON
#             data = r.json()
#             articles = data.get('articles',[])
#             for article in articles:
#                 speak(article['title'])
#     else:
#         #Let it handle by OpenAl
#         output = ask_llm(c)
#         speak(output)


# if __name__ == "__main__":
#     speak("Initializin"phantom....")  



#     while True:
#         #Obtaining audio from microphone
#         #Listen to wake word"phantom"

#         r = sr.Recognizer()
#         print("recognizing....")

#         try:
#             with sr.Microphone() as source:
#                 print("Listening....")
#                 audio = r.listen(source, timeout=2,phrase_time_limit=1)
#             word = r.recognize_google(audio)
#             if (word.lower() =="phantom"):
#                 speak("Ya")
#                 #Listen For Command
#                 with sr.Microphone() as source:
#                     print("Google Active....")
#                     audio  = r.listen(source)
#                     command = r.recognize_google(audio)
#                     processCommand(command)

                
#         except Exception as e:
#             print("Error; {0}".format(e))
import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import os
import requests
from gtts import gTTS
import pygame
import music_library
import google.generativeai as genai
from flask import Flask, render_template, jsonify
import threading
from client import ask_llm
from dotenv import load_dotenv

load_dotenv()
# ---------------- FLASK ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- FLAGS ----------------
running = False
assistant_thread = None

# ---------------- ORIGINAL SETUP ----------------
recognizer = sr.Recognizer()
pygame.mixer.init()

NEWS_API_KEY=os.getenv("NEWS_API_KEY")

# ---------------- SPEAK (UNCHANGED) ----------------
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# ---------------- AI (UNCHANGED) ----------------
# def ask_llm(command):
#     prompt = f"You are a virtual assistant named Phantom. Answer in short.\n{command}"
#     response = model.generate_content(prompt)
#     return response.text

# ---------------- COMMANDS (UNCHANGED) ----------------
def processCommand(c):
    c = c.lower()

    if "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")

    elif "open github" in c:
        webbrowser.open("https://github.com")

    elif "open notepad" in c:
        os.system("notepad")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        link = music_library.music.get(song)
        if link:
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
            speak("Here are the top news headlines")
            for article in articles[:5]:
                speak(article["title"])
        else:
            speak("Unable to fetch news")

    else:
        reply = ask_llm(c)
        speak(reply)

# ---------------- MAIN LOOP (WRAPPED ONLY) ----------------
def phantom_loop():
    global running
    speak("Initializing Phantom.....")

    while running:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)

            wake_word = recognizer.recognize_google(audio)

            if wake_word.lower() == "phantom":
                speak("Yes....Listening!!")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                processCommand(command)

        except Exception:
            pass

# ---------------- API CONTROL ----------------
@app.route("/start", methods=["POST"])
def start():
    global running, assistant_thread
    if not running:
        running = True
        assistant_thread = threading.Thread(target=phantom_loop)
        assistant_thread.start()
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    global running
    running = False
    return jsonify({"status": "stopped"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)

        

