import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = [
    {"role": "system", "content": "You are a medical assistant helping doctors understand symptoms."}
]

def chat_with_bot(user_input: str):
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key not configured")
    # Rest of the function remains the same
    ...