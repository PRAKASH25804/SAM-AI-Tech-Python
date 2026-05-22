import os
import random
import subprocess
import webbrowser

import requests
import pyttsx3
import speech_recognition as sr
import wikipedia
from datetime import datetime

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

JOKES = [
    "Why did the computer show up at work late? It had a hard drive.",
    "I told my computer I needed a break, and it said no problem — it needed one too.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
]

APPLICATIONS = {
    "calculator": "calc.exe",
    "notepad": "notepad.exe",
    "browser": None,
}


def speak(message: str):
    print(f"Assistant: {message}")
    engine.say(message)
    engine.runAndWait()


def listen_command(timeout: int = 5, phrase_time_limit: int = 7) -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("I did not understand the audio.")
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
        except Exception as ex:
            print(f"Error recording audio: {ex}")
    return ""


def get_time() -> str:
    return datetime.now().strftime("%I:%M %p")


def open_website(url: str):
    webbrowser.open(url)


def search_wikipedia(query: str) -> str:
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as details:
        return f"The topic is ambiguous. Try one of these: {details.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "I could not find a page for that topic."
    except Exception:
        return "An error occurred while searching Wikipedia."


def tell_joke() -> str:
    return random.choice(JOKES)


def fetch_weather(city: str) -> str:
    if not city:
        return "Please provide a city name."
    try:
        response = requests.get(f"http://wttr.in/{city}?format=3", timeout=8)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return "Sorry, I could not fetch weather information right now."


def open_application(app_name: str) -> bool:
    if not app_name:
        return False
    app_key = app_name.strip().lower()
    if app_key in APPLICATIONS:
        executable = APPLICATIONS[app_key]
        try:
            if executable:
                os.startfile(executable)
            else:
                webbrowser.open("https://www.google.com")
            return True
        except Exception:
            return False
    if os.name == "nt":
        try:
            os.startfile(app_key)
            return True
        except Exception:
            return False
    try:
        subprocess.Popen([app_key])
        return True
    except Exception:
        return False
