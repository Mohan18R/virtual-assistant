import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import requests
import threading
import os
import sys
import time
import wikipedia
import webbrowser
from gesture_control import start_gesture_control

# Global states
SILENT_MODE = False
ENERGY_THRESHOLD = 400
PAUSE_THRESHOLD = 0.8

en = pyttsx3.init()
en.setProperty('rate', 180)
en.setProperty('volume', 1.0)

def speak(text):
    """Thread-safe speech output"""
    def _speak():
        try:
            en.say(text)
            en.runAndWait()
        except RuntimeError:
            en.endLoop()
            en.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()
    print(f"Assistant: {text}")





def fetch_answer(query):
    """Fetch answer from Wikipedia, otherwise perform a Google search"""
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary[:250])
    except wikipedia.exceptions.DisambiguationError:
        speak("Too many results. Try being more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find an answer. Searching on Google.")
        webbrowser.open(f"https://www.google.com/search?q={query}")




def find_applications():
    """Discover installed applications"""
    apps = {
        'vs code': ['code', 'C:\\Program Files\\Microsoft VS Code\\Code.exe'],
        'word': ['winword', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE'],
        'powerpoint': ['powerpnt', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE']
    }
    discovered = {}
    for name, paths in apps.items():
        for path in paths:
            if os.path.exists(path) or subprocess.call(f"where {path}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                discovered[name] = path
                break
    return discovered

APPS = find_applications()

def open_application(app_name):
    """Launch applications or open web apps"""
    web_apps = {'youtube': 'https://youtube.com', 'whatsapp': 'https://web.whatsapp.com'}
    if app_name in web_apps:
        webbrowser.open(web_apps[app_name])
        speak(f"Opening {app_name}")
    elif app_name in APPS:
        subprocess.Popen(APPS[app_name], shell=True)
        speak(f"Opening {app_name}")
    else:
        speak("Application not found.")

def process_command(cmd):
    """Process user commands"""
    global SILENT_MODE
    cmd = cmd.lower().strip()
    if 'open' in cmd:
        open_application(cmd.replace('open', '').strip())
    elif 'search' in cmd:
        query = cmd.replace('search', '').strip()
        webbrowser.open(f"https://google.com/search?q={query}")
        speak(f"Searching for {query}")
    elif any(q in cmd for q in ['what is', 'how to']):
        fetch_answer(cmd)
    elif 'gesture mode' in cmd:
        speak("Activating gesture control")
        threading.Thread(target=start_gesture_control, daemon=True).start()
        SILENT_MODE = True
    elif 'silent mode' in cmd:
        SILENT_MODE = True
        speak("Silent mode activated. Say 'wake up' to disable.")
    elif 'wake up' in cmd:
        SILENT_MODE = False
        speak("I'm listening.")
    elif 'exit' in cmd:
        speak("Shutting down.")
        sys.exit()
    else:
        speak("Command not recognized.")

def listen_loop():
    global SILENT_MODE
    """Continuously listen for commands, even in silent mode"""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = ENERGY_THRESHOLD
    recognizer.pause_threshold = PAUSE_THRESHOLD
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            try:
                print("\n[ Listening ]")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()
                
                if SILENT_MODE:
                    if "wake up" in command:
                        
                        SILENT_MODE = False
                        speak("I'm listening.")
                    continue  # Keep waiting for "wake up"
                
                print(f"User: {command}")
                process_command(command)

            except sr.UnknownValueError:
                continue  # Ignore if nothing is heard
            except sr.RequestError:
                speak("Check your internet connection.")
            except Exception:
                print("Restarting listener...")
                time.sleep(2)


if __name__ == "__main__":
    print("\n=== AI Assistant Initialized ===\n")
    speak("System online. How can I assist you today?")
    listen_loop()
        
