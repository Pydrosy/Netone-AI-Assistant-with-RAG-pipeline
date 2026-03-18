import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"Key length: {len(api_key) if api_key else 0}")

# Groq API endpoint
url = "https://api.groq.com/openai/v1/chat/completions"

# Correct headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Correct request body format
data = {
    "model": "mixtral-8x7b-32768",  # Make sure this model is available
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Groq API is working!' in one sentence."}
    ],
    "temperature": 0.1,
    "max_tokens": 50
}

print(f"\nSending request to Groq...")
print(f"Model: {data['model']}")

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Response: {result['choices'][0]['message']['content']}")
    else:
        print(f"\n❌ Error {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")