# Virtual Assistant

An intelligent AI assistant that combines **voice recognition** and **hand gesture control** to perform system automation, open applications, search the web, and control media playback hands-free.

## 🚀 Features
- **Voice-Controlled AI Assistant**: Uses **SpeechRecognition** and **pyttsx3** for natural language interactions.
- **Gesture-Based System Control**: Utilizes **OpenCV** and **MediaPipe** to detect hand gestures for controlling volume, media playback, and navigation.
- **Automated System Interactions**: Integrates **PyAutoGUI** for executing commands triggered by voice and gestures.
- **Wikipedia & Web Search**: Fetches concise answers from **Wikipedia** or opens a **Google search** when needed.
- **Application Launcher**: Opens installed applications like VS Code, Word, and web apps like YouTube and WhatsApp.

## 🛠️ Tech Stack
- **Python**
- **SpeechRecognition**
- **pyttsx3**
- **OpenCV**
- **MediaPipe**
- **PyAutoGUI**
- **Wikipedia API**

## 🎯 How It Works
### 1️⃣ Voice Commands
- Say "Open VS Code" to launch VS Code.
- Say "Search Python tutorials" to get results on Google.
- Say "Gesture mode" to activate hand tracking.
- Say "Silent mode" to stop voice responses.
- Say "Wake up" to resume listening.

### 2️⃣ Hand Gestures (in Gesture Mode)
- **Move Cursor**: Index finger up, all others down.
- **Click**: Thumb up, all other fingers down.
- **Volume Control**: Adjusts based on distance between fingers.
- **Swipe Left/Right**: Moves slides/media using specific hand signs.
- **Take Screenshot**: Perform a specific hand gesture.

## 🏗️ Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo.git
   cd ai-assistant-gesture
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the assistant**
   ```bash
   python main.py
   ```

## 📌 Future Enhancements
- **Context-aware voice responses**
- **More refined hand gesture actions**
- **GUI for better user experience**

## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Feel free to fork, submit issues, and send pull requests!

---


