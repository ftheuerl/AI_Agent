import os

from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Gemini_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )

    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("API request failed")
#    user_prompt = contents
    prompt_tokens = usage_metadata.prompt_token_count
    response_tokens = usage_metadata.candidates_token_count

#    print(user_prompt)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()

