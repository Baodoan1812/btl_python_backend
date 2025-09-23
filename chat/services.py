import requests
import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()
GROQ_API_KEY= os.getenv("GROQ_API_KEY")
def call_ai_api(user_message: str) -> str:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + GROQ_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Always reply in Vietnamese."},
                {"role": "user", "content": user_message}
            ]
        }
    )
    data = response.json()
    print("DEBUG Groq response:", data)
    print("DEBUG GROQ_API_KEY:", GROQ_API_KEY)
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    elif "error" in data:
        return f"Chatbot error: {data['error']['message']}"
    else:
        return "Unexpected response from Groq"
