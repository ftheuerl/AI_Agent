import os
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, schema_get_files_info
from call_function import available_functions, call_function

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():

# ===== POINT 1: Argument parsing =====
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

# ===== POINT 2: Initial messages list creation =====
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

# ===== POINT 3: Loading env vars and creating client =====
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Gemini_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)

# ===== Looping point ====
#    got_final_response == False
    for _ in range(20):

# ===== POINT 4: Calling generate_content =====
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
            )
        )

# ===== POINT 5: Handling the response =====
        usage_metadata = response.usage_metadata
        if usage_metadata is None:
            raise RuntimeError("API request failed")
        for candidate in response.candidates:
            messages.append(candidate.content)


#        prompt_tokens = usage_metadata.prompt_token_count - not in use anymore
#        response_tokens = usage_metadata.candidates_token_count - not in use anymore


        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception('Error: parts returned as None')
                f_response = function_call_result.parts[0].function_response
                if f_response is None:
                    raise Exception('Error: No FunctionResponse object')
                if f_response.response is None:
                    raise Exception('Error: No function result')
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))

        else:
            print("Response:")
            print(response.text)
            break
    else:
        print("Hit maximum iterations without reaching a final response")
        exit(1)


if __name__ == "__main__":
    main()

