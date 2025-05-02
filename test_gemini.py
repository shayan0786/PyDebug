import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    print("Error: No GEMINI_API_KEY found in .env file")
    exit(1)

try:
    genai.configure(api_key=API_KEY)
    
    # List available models first
    print("Available models:")
    for m in genai.list_models():
        print(f"- {m.name}")
    
    # Use the correct model name
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content("Say 'test'")
    print("\nAPI test successful!")
    print(response.text)
except Exception as e:
    print(f"\nAPI test failed: {str(e)}")