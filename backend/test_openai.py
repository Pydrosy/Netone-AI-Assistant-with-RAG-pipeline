import openai
from app.config import settings

# Test the API key
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

try:
    # Simple test
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'API key is working!'"}],
        max_tokens=20
    )
    print(f"✅ API Key is working!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")