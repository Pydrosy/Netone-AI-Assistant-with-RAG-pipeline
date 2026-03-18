import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"✅ API Key loaded")

# Models from your list that should work for chat
models_to_test = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "qwen/qwen3-32b",
    "moonshotai/kimi-k2-instruct"
]

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("\n🔍 Testing available models...\n")

working_model = None

for model in models_to_test:
    print(f"📡 Testing: {model}")
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Say 'This model works!' in one short sentence"}
        ],
        "temperature": 0.1,
        "max_tokens": 20
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! Response: {result['choices'][0]['message']['content']}")
            working_model = model
            break
        else:
            error_data = response.json()
            print(f"❌ Failed: {error_data.get('error', {}).get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

if working_model:
    print(f"\n🎯 Recommended model: {working_model}")
    print("\nAdd this to your .env file:")
    print(f"GROQ_MODEL={working_model}")
else:
    print("\n❌ No working model found. Try running the comprehensive test.")
