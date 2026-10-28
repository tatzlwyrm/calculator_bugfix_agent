import os
from dotenv import load_dotenv
from openai import OpenAI

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
user_prompt = input("Question or prompt: ") + " Limit the response to one paragraph."
#"What is the calendar window over which you have reliable information? What can you tell me about the Boot.dev course release schedule? Answer in one paragraph only. "

# Get a response from the model, which will be at response.choices[0].message.content . 
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": user_prompt,
            #"What are the easiest ways to supplement the Boot.dev AI engineering courses? Use one paragraph maximum."
            #"What highly-anticipated and useful (non-meme) crypto projects are entering mainnet or issuing airdrops in November 2026? Use one paragraph maximum.",
        }
    ],
)

# Verify lack of API response.
if response.usage == None:
    raise RuntimeError("response.usage is None, possible API response failure?")

# Define main function. 
def main():
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"Response: {response.choices[0].message.content}")

# Run main function if file is not loaded as a library. 
if __name__ == "__main__":
    main()
