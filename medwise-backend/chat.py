import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = [
    {"role": "system", "content": "You are a medical assistant helping doctors understand symptoms."}
]

def chat_with_bot(user_input: str):
    chat_history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_history,
        temperature=0.7
    )
    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    return reply
