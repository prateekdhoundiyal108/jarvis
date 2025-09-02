# Jarvis Voice Assistant

Jarvis is a Python-based voice assistant that uses Google Gemini AI for intelligent responses and Google Cloud Text-to-Speech for high-quality voice output. It can recognize voice commands, answer questions, open websites, and play music from a predefined library.

## Features

- Wake word detection ("Jarvis")
- Voice command recognition using `speech_recognition`
- AI-powered responses via Google Gemini
- High-quality speech synthesis with Google Cloud Text-to-Speech
- Opens popular websites (Google, YouTube, Facebook, LinkedIn, Gemini)
- Plays songs from a customizable music library
- Extensible for custom actions via AI instructions

## Setup

1. **Clone the repository**  
- git clone https://github.com/prateekdhoundiyal108/jarvis.git cd Jarvis Project

2. **Install dependencies**  
- pip install -r requirements.txt

3. **Google Cloud Setup**  
- Create a Google Cloud project and enable Text-to-Speech API.
- Download your service account credentials as `credentials.json` and place it in the project directory.

4. **Google Gemini API Setup**  
- Get your Gemini API key and add it to a `.env` file:
  ```
  GEMINI_API_KEY=your-gemini-api-key
  ```

5. **Run the assistant**  
- python main.py

## Files

- `main.py` — Main entry point, voice recognition and command processing
- `ai_module.py` — Handles communication with Google Gemini AI
- `musicLibrary.py` — Contains the music library
- `list_models.py` — Lists available Gemini models
- `.env` — Stores API keys (not tracked by git)
- `credentials.json` — Google Cloud credentials (not tracked by git)

## Notes

- `.env` and `credentials.json` are excluded from version control for security.
- Requires a working microphone and internet connection.

## License

MIT License