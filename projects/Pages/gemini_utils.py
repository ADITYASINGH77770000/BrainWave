import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

def configure_gemini():
    """Configures the Gemini API using the environment variable."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return False
    
    genai.configure(api_key=api_key)
    return True

def get_gemini_response(prompt, image):
    """Generates a response from the Gemini API for the given prompt and image."""
    try:
        # Convert image to bytes
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()
        
        # Create a request
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content([prompt, img_bytes])
        
        return response.text if response else "No response received."
    except Exception as e:
        return f"Error generating response: {e}"
