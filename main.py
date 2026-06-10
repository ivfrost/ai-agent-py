import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
load_dotenv()

def generate_content(client, messages):
    config = types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools=[available_functions])
    return client.models.generate_content(
        model="gemini-2.5-flash", contents=messages, config=config,
    )

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    
    client = genai.Client(api_key=api_key)
    response = generate_content(client, messages)
    usageMeta = response.usage_metadata
    if not usageMeta:
        raise RuntimeError("API request failed. Try again later")
    
    promptTokens = usageMeta.prompt_token_count
    responseTokens = usageMeta.candidates_token_count
    if args.verbose:
        print("Prompt tokens: " + str(promptTokens)) 
        print("Response tokens: " + str(responseTokens)) 
        print()
        print("User prompt: " + str(args.user_prompt))
        print()
    func_results = []
    if response.function_calls:
        for func in response.function_calls:
            function_call_result = call_function(func, args.verbose);
            if not function_call_result.parts:
                raise ValueError("Missing .parts list on function_call result")
            function_response = function_call_result.parts[0].function_response
            if not function_response:
                raise ValueError("Missing function_response on parts' first index")
            if not function_response.response:
                raise ValueError("Missing result of function call")
            func_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_response.response}")

    else:
        print(response.text)


if __name__ == "__main__":
    main()
