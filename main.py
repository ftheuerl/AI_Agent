import os
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, schema_get_files_info
from functions.call_function import available_functions

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
    contents=messages,
    #config=types.GenerateContentConfig(
    #system_instruction=system_prompt,
    #temperature=0),
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt #new add
        )
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
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()

