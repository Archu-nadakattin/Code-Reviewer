import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API key loaded:", bool(api_key))

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=30000
    )
)

print("Sending request...")

try:

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say hello in one short sentence.",
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
            temperature=0.2,
            max_output_tokens=50
        )
    )

    print("\n========== RESPONSE OBJECT ==========")
    print(response)

    print("\n========== TEXT ==========")
    print(repr(response.text))

    print("\n========== CANDIDATES ==========")
    print(response.candidates)

    print("\n========== PROMPT FEEDBACK ==========")
    print(response.prompt_feedback)

    if response.candidates:

        print("\n========== FIRST CANDIDATE ==========")

        candidate = response.candidates[0]

        print(candidate)

        if candidate.content:
            print("\n========== PARTS ==========")
            print(candidate.content.parts)

            for part in candidate.content.parts:
                print("\nPART:")
                print(part)

except Exception as e:

    print("\n========== ERROR ==========")
    print(type(e).__name__)
    print(str(e))

    #test