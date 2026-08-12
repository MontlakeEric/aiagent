import argparse
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions
from call_functions import call_function

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("API key not found in environment variables")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the chatbot")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {
        "role": "system",
        "content": system_prompt,
    },
    {
        "role": "user",
        "content": args.user_prompt,
    }
]

result = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)

if result.usage is None:
    raise RuntimeError("No usage information returned from the API, indicating it may have failed.")

if args.verbose:
    print(f"User prompt: {messages[0]['content']}")
    print(f"Prompt tokens: {result.usage.prompt_tokens}")
    print(f"Response tokens: {result.usage.completion_tokens}")   

message = result.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose=args.verbose)
        if not result_message["content"]:
            raise RuntimeError(f"Function call {tool_call.function.name} returned no content")
        if args.verbose:
            print(f"-> {result_message['content']}")
else:
    print(message.content)
