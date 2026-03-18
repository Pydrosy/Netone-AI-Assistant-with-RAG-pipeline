# test_groq_available_models.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {"Authorization": f"Bearer {api_key}"}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        models = response.json()
        print("✅ Available Groq models:")
        for model in models['data']:
            print(f"  - {model['id']} (context: {model.get('context_length', 'N/A')})")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Exception: {e}")