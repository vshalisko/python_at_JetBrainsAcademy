import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key_old = os.environ.get("OPENAI_API_KEY", None)
api_key = os.environ.get("OPENROUTER_API_KEY", None)

from openai import OpenAI

MODEL_35_TURBO = "gpt-3.5-turbo-0125"
MODEL_4_TURBO = "gpt-4-turbo-2024-04-09"

MODELS = {
    MODEL_35_TURBO: {"input_cost": 0.5 / 1000000, "output_cost": 1.5 / 1000000},
    MODEL_4_TURBO: {"input_cost": 10.0 / 1000000, "output_cost": 30.0 / 1000000},
}

functions_list = [
    {
        "type": "function",
        "function": {
            "name": "end_conversation",
            "description": "Finish the current conversation by user request, when he says End conversation",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]

client = OpenAI(api_key=api_key,
                base_url="https://openrouter.ai/api/v1")

def get_chat_completion(messages, tools=None, tool_choice="auto"):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
        #temperature=0.7
    )

def calculate_tokens_cost(model, chat_completion):
    if model not in MODELS:
        raise ValueError(f"Model {model} is not supported.")

    model_costs = MODELS[model]
    input_tokens_cost = chat_completion.usage.prompt_tokens * model_costs["input_cost"]
    output_tokens_cost = (
        chat_completion.usage.completion_tokens * model_costs["output_cost"]
    )
    return input_tokens_cost + output_tokens_cost

def end_conversation():
    return False

function_list = {
    "end_conversation":end_conversation
}

conversation_ok = True

while conversation_ok:

    prompt = input("Enter a message: ")

    messages = [    {
        "role": "system",
        "content": "Call a funcion only when user ask to end conversation.",
    },
        {"role": "user", "content": prompt}]

    completion = get_chat_completion(messages, tools=functions_list)
    gpt_message = completion.choices[0].message
    gpt_response = gpt_message.content
    total_usage_costs = calculate_tokens_cost(MODEL_35_TURBO, completion)

    # Extract the tool_calls content
    if gpt_message.tool_calls:
        tool_call = gpt_message.tool_calls[0]
        # Extract the function name and the arguments
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        # Get the actual function
        function_to_call = function_list[function_name]
        # Call the function with the parameter(s) and store the function response
        conversation_ok = function_to_call()
        print(tool_call.id)

    print("You:", prompt)
    print("Assistant:", gpt_response)
    print(f"Cost: ${total_usage_costs:.8f}\n")
