import os
from dotenv import load_dotenv

load_dotenv()

api_key_old = os.environ.get("OPENAI_API_KEY", None)
api_key = os.environ.get("OPENROUTER_API_KEY", None)

from openai import OpenAI

client = OpenAI(api_key=api_key,
                base_url="https://openrouter.ai/api/v1")

def get_chat_completion(messages):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7  # A non-zero temperature for randomness
    )

prompt = "What are you?"
messages = [{"role": "user", "content": prompt}]

chat_completion = get_chat_completion(messages)
gpt_response = chat_completion.choices[0].message.content

print("You:", prompt)
print("Assistant:", gpt_response)
