# list_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

try:
    # Get the API key from the environment variable
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY was not found. Please check your .env file.")
    else:
        genai.configure(api_key=api_key)

        print("--- Available Models ---")
        for m in genai.list_models():
          if 'generateContent' in m.supported_generation_methods:
            print(m.name)
        print("------------------------")

except Exception as e:
    print(f"An error occurred: {e}")