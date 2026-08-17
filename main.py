import argparse
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions
from call_functions import call_function

def main():
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found in environment variables")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

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

    done = False
    for _ in range(20):
        if (done := make_call(messages, client, args.verbose)):
            break
    if not done:
        print("Error: Maximum number of iterations reached without completing the conversation.")
        exit(1)

def make_call(messages: list, client: OpenAI, verbose: bool) -> bool:

    result = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if result.usage is None:
        raise RuntimeError("No usage information returned from the API, indicating it may have failed.")

    if verbose:
        print(f"User prompt: {messages[0]['content']}")
        print(f"Prompt tokens: {result.usage.prompt_tokens}")
        print(f"Response tokens: {result.usage.completion_tokens}")   

    message = result.choices[0].message

    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=verbose)
            if not result_message["content"]:
                raise RuntimeError(f"Function call {tool_call.function.name} returned no content")
            messages.append(result_message)
            if verbose:
                print(f"-> {result_message['content']}")
            return False
    else:
        print(message.content)
        return True

if __name__ == "__main__":
    main()
