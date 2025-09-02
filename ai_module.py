# ai_module.py

import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load the environment variables from the .env file
load_dotenv()

def ask_ai(query):
    """Sends a query to the Google Gemini model and returns the response."""
    try:
        # Get the API key from the environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return "Error: GEMINI_API_KEY was not found. Please check your .env file."

        genai.configure(api_key=api_key) 
        
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(query)

        instructed_query = "Keep your answer to two sentences or less. " + query
        
        response = model.generate_content(instructed_query)
        
        try:
            # Clean up the response to make it valid JSON
            clean_response = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_response)
            return data # Return the dictionary
        except json.JSONDecodeError:
            # If it's not JSON, return the plain text
            return response.text
            
    except Exception as e:
        print(f"Error communicating with AI: {e}")
        return "Sorry, I am having trouble connecting to my brain right now."