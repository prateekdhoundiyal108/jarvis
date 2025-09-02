import speech_recognition as sr
import webbrowser
import subprocess
import musicLibrary
import ai_module 
from google.cloud import texttospeech
import pygame
import os


from dotenv import load_dotenv

load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'


def speak(text):
    """Speaks the given text using Google's high-quality AI voice."""
    try:
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select a language code ("en-US") and the ssml
        # voice gender ("neutral"). For other voices, see the documentation.
        # This uses a high-quality WaveNet voice.
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Wavenet-D"
        )

        # Select the type of audio file you want
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary. We'll play it with pygame.
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Write the binary audio content to a temporary file
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')

        # Load and play the audio file
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error in speak function: {e}")

def processCommand(c):
    command = c.lower()
    if "goodbye" in command or "leave" in command:
        speak("Goodbye! Shutting down.")
        return "exit"
    elif "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open linkdin" in command:
        webbrowser.open("https://linkdin.com")
    elif "open gemini" in command:
        webbrowser.open("https://gemini.google.com/app")
    elif command.startswith("play"):
        song = command.replace('play', '').strip()
        link = musicLibrary.music[song]
        webbrowser.open(link)
    else:
        # Send the command to the AI, which might return text OR a dictionary
        response = ai_module.ask_ai(command)
        
        # Check if the response is a dictionary (a command instruction)
        if isinstance(response, dict) and response.get("action") == "open_website":
            url_to_open = response.get("url")
            if url_to_open:
                speak(f"Opening {url_to_open.split('//')[1]}...")
                subprocess.run(["open", url_to_open])
            else:
                speak("The AI told me to open a website, but didn't provide a URL.")
        # Otherwise, if it's just a string, speak it
        elif isinstance(response, str):
            speak(response)
              
    
is_conversing = False
recognizer = sr.Recognizer()

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    # Listen for the wake word 'Jarvis'
    
while True:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Step 1: Listen for the wake word ONLY if not already in a conversation
            if not is_conversing:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
                wake_word = recognizer.recognize_google(audio)
                
                if 'jarvis' not in wake_word.lower():
                    continue # If no wake word, restart the loop

            # Step 2: Now that Jarvis is awake, listen for a command
            speak("Yes?")
            is_conversing = True # Enter conversation mode
            
            print("Listening for your command...")
            command_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(command_audio)
            
            result = processCommand(command)

            if result == "exit":
                break   

    except sr.WaitTimeoutError:
        # If the user stops talking, exit conversation mode
        if is_conversing:
            print("User silent, returning to wake word mode.")
            is_conversing = False
        continue # Restart the loop
        
    except sr.UnknownValueError:
        # If speech is not understood, prompt again if in conversation
        if is_conversing:
            speak("Sorry, I didn't quite catch that.")
        continue # Restart the loop
        
    except Exception as e:
        print(f"An error occurred: {e}")
        break