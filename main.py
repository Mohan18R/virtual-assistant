import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import requests
from bs4 import BeautifulSoup
from gesture_control import start_gesture_control
import sys

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speaks the given text."""
    engine.say(text)
    engine.runAndWait()

# Voice Command Functions
def open_application(app_name):
    """Opens specific applications based on the command."""
    try:
        if "vs code" in app_name:
            subprocess.Popen(["code"])
            speak("Opening Visual Studio Code.")
        elif "youtube" in app_name:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")
        elif "whatsapp" in app_name:
            webbrowser.open("https://web.whatsapp.com")
            speak("Opening WhatsApp.")
        elif "word" in app_name:
            subprocess.Popen(["start", "winword"], shell=True)
            speak("Opening Microsoft Word.")
        elif "powerpoint" in app_name:
            subprocess.Popen(["start", "powerpnt"], shell=True)
            speak("Opening Microsoft PowerPoint.")
        elif "pilot" in app_name:
            speak("Starting gesture control mode.")
            start_gesture_control()
            speak("Gesture control mode is now active. Say 'Hey Assistant' to continue.")
            return "silent"  # Stop listening
        else:
            speak("Application not recognized.")
    except Exception as e:
        speak(f"Unable to open {app_name}.")

def fetch_answer(query):
    """Fetches answers from Google for general queries."""
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        answer = soup.find("div", class_="BNeawe").text
        speak(answer)
    except Exception as e:
        speak("I couldn't find the answer to that. Please try again.")

def process_command(command):
    """Processes the user command."""
    if "open" in command:
        app_name = command.replace("open", "").strip()
        result = open_application(app_name)
        if result == "silent":
            return "silent"
    elif "search" in command:
        search_query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching for {search_query} on Google.")
    elif "what is" in command or "how is" in command:
        fetch_answer(command)
    elif "quit" in command:
        speak("Goodbye! Have a great day.")
        sys.exit()
    else:
        speak("I didn't understand that command. Please try again.")
    return "active"

def listen_for_commands(silent_mode=False):
    """Listens for user commands continuously."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        if not silent_mode:
            speak("Listening for your commands now.")
        while True:
            try:
                print("Listening for commands..." if not silent_mode else "Silent mode active.")
                audio = recognizer.listen(source)
                user_command = recognizer.recognize_google(audio).lower()
                
                if silent_mode and "hey assistant" in user_command:
                    speak("Yes, I am listening. Tell me what to do.")
                    silent_mode = False
                elif not silent_mode:
                    silent_mode = process_command(user_command) == "silent"
            except sr.UnknownValueError:
                if not silent_mode:
                    speak("Sorry, I didn't catch that. Please repeat.")
            except sr.RequestError:
                speak("Network error. Please check your internet connection.")
                break

# Start the assistant
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("Say 'Hey Assistant' to start.")
        try:
            print("Waiting for wake word...")
            audio = recognizer.listen(source)
            wake_word = recognizer.recognize_google(audio).lower()

            if "hey assistant" in wake_word:
                speak("Yes, I am listening. Tell me what to do.")
                listen_for_commands()
        except sr.UnknownValueError:
            speak("I couldn't understand. Please try again.")
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
