import os
import argparse

from dotenv import load_dotenv
from google import genai
#new add to start creating a history of messages
from google.genai import types


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
# Now we can access `args.user_prompt`

# new add to create memory of messages
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Gemini_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages
    )

    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("API request failed")

    prompt_tokens = usage_metadata.prompt_token_count
    response_tokens = usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()

