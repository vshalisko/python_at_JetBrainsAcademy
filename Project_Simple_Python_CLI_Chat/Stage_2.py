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

MODEL_35_TURBO = "gpt-3.5-turbo"
MODEL_4_TURBO = "gpt-4-turbo-preview"

MODELS = {
    MODEL_35_TURBO: {"input_cost": 0.0005 / 1000, "output_cost": 0.0015 / 1000},
    MODEL_4_TURBO: {"input_cost": 0.01 / 1000, "output_cost": 0.03 / 1000},
}

def calculate_tokens_cost(model, chat_completion):
    if model not in MODELS:
        raise ValueError(f"Model {model} is not supported.")

    model_costs = MODELS[model]
    input_tokens_cost = chat_completion.usage.prompt_tokens * model_costs["input_cost"]
    output_tokens_cost = (
        chat_completion.usage.completion_tokens * model_costs["output_cost"]
    )
    return input_tokens_cost + output_tokens_cost

#prompt = "What are you?"
prompt = input("Enter a message: ")
messages = [{"role": "user", "content": prompt}]

chat_completion = get_chat_completion(messages)
gpt_response = chat_completion.choices[0].message.content

print("You:", prompt)
print("Assistant:", gpt_response)

total_usage_costs = calculate_tokens_cost(MODEL_35_TURBO, chat_completion)
print(f"Cost: ${total_usage_costs:.8f}")
