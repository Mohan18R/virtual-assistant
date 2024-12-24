# Virtual Assistant

A Python-based intelligent virtual assistant that enables users to control applications and access information using voice commands and hand gestures. This project combines voice recognition, text-to-speech, gesture control, and web scraping to deliver an intuitive, multimodal user experience.

## Features

- **Voice-Controlled Commands**  
  - Open applications like YouTube, WhatsApp, Microsoft Word, and PowerPoint.
  - Perform web searches and fetch answers to general queries.
  - Real-time speech-to-text and text-to-speech capabilities.

- **Gesture-Based Control**  
  - Integrated with MediaPipe for hand tracking and gesture recognition.
  - Control system functions like volume adjustment, media playback, and navigation using hand gestures.

- **Web Scraping**  
  - Fetch real-time information from Google using BeautifulSoup.
  - Provide spoken answers to user questions.

- **Scalable and Modular**  
  - Designed to accommodate future features like expanded application support and advanced gesture recognition.

## Technologies Used

- **Python** for backend scripting.
- **SpeechRecognition** for voice command input.
- **pyttsx3** for text-to-speech output.
- **OpenCV** and **MediaPipe** for hand gesture recognition.
- **PyAutoGUI** for system interaction via gestures.
- **BeautifulSoup** for web scraping to fetch answers.

## How It Works

1. **Voice Commands:**  
   - The assistant listens for commands and responds by executing the appropriate actions, such as opening applications or searching the web.

2. **Gesture Control:**  
   - Hand gestures are detected using a webcam, allowing for control of system functions without physical input.

3. **Information Retrieval:**  
   - General queries are processed via web scraping, and the assistant provides real-time spoken answers.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries:
  - `speechrecognition`
  - `pyttsx3`
  - `opencv-python`
  - `mediapipe`
  - `pyautogui`
  - `pycaw`
  - `beautifulsoup4`
  - `requests`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mohan18R/virtual-assistant.git
