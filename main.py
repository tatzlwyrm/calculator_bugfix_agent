import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from config import TEMPERATURE
import json
from call_function import available_functions

# Interpret command-line string argument as the user prompt.
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Load .env variables such as the API key secret.
# Be sure .env is in .gitignore.
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("API key cannot be None!")

# Create a client after loading the OpenAI library.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# User prompt or question.
#user_prompt = input("Question or prompt: ") + " Limit the response to one paragraph."
#"What is the calendar window over which you have reliable information? What can you tell me about the Boot.dev course release schedule? Answer in one paragraph only. "

session_messages = [\
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

# Get a response from the model, which will be at response.choices[0].message.content .
response = client.chat.completions.create(
    model="openrouter/free",
    messages=session_messages,
    temperature=TEMPERATURE,
    tools=available_functions,
)

message = response.choices[0].message

# Verify lack of API response.
if response.usage == None:
    raise RuntimeError("response.usage is None, possible API response failure?")

# Define main function.
def main():
    if args.verbose:
        print("Verbose mode on.")
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    if message.tool_calls != None:
        print(f"Message Tool Calls: True")
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(f"Response: {response.choices[0].message.content}")

# Run main function if file is not loaded as a library.
if __name__ == "__main__":
    main()
