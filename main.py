import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from config import TEMPERATURE
import json
import sys
from call_function import available_functions, call_function
#n


def parse_arguments():
    # Interpret command-line string argument as the user prompt.
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def initiate_client():
    # Load .env variables such as the API key secret.
    # Be sure .env is in .gitignore.
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("API key cannot be None!")

    # Create a client after loading the OpenAI library.
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


# Get a response from the model, which will be at response.choices[0].message.content .
def get_model_response(client, session_messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=session_messages,
        temperature=TEMPERATURE,
        tools=available_functions,)
    # Verify if lack of API response.
    if response.usage == None:
        raise RuntimeError("response.usage is None, possible API response failure?")
    return response


# Define main function.
def main():
    args = parse_arguments()
    messages = [\
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},]
    client = initiate_client()
    # User prompt or question.
    #user_prompt = input("Question or prompt: ") + " Limit the response to one paragraph."
    #"What is the calendar window over which you have reliable information? What can you tell me about the Boot.dev course release schedule? Answer in one paragraph only. "
    max_loops = 20
    #messages = []
    while max_loops > 0:
        response = get_model_response(client, messages)
        message = response.choices[0].message
        messages.append(message)
        print(messages)
        #print(f"message type is {type(message)}")
        if args.verbose:
            print("Verbose mode on.")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        if not message.tool_calls:
            print(f"Response: {response.choices[0].message.content}")
            print(f"Error: Tool calls exhausted.")
            sys.exit(0)
        #elif message.tool_calls is []:
        else:
            print(f"Message Tool Calls: True")
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Function arguments: {function_args}")
                result_message = call_function(tool_call, args.verbose)
                if result_message['content'] == None:
                    raise Exception("Error: tool message content is None.")
                messages.append(result_message)
                print(f"Result message: {result_message}")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                #print(f"Calling function: {tool_call.function.name}({function_args})")

        max_loops -= 1
    sys.exit(1)


# Run main function if file is not loaded as a library.
if __name__ == "__main__":
    main()
