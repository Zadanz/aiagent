import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if (api_key is None):
        raise RuntimeError("No API key found")

    # Argument handling
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    
    verbose_output = args.verbose
    prompt = args.user_prompt

    # AI access
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(20):

        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages, 
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0)        
            )
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(f"\n{candidate.content}")

        if (response.usage_metadata is None):
            raise RuntimeError("Request failure, API service might be down.")

        if verbose_output:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
        
        # Print AI response
        function_responses = []

        if response.function_calls:   
            for func in response.function_calls:
                function_call_result = call_function(func, verbose=verbose_output)

                if not function_call_result.parts:
                    raise Exception("Error: Function Call result parts empty")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Error: Function Call result has no function response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Error: Function Call result has no response")

                function_responses.append(function_call_result.parts[0])

                if verbose_output:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

        else:
            print(response.text)
            return("Success")

        messages.append(types.Content(role="user", parts=function_responses))
    print("Took Gemini too long to finish. Reached cut-off point.")
    exit(1)




if __name__ == "__main__":
    main()
