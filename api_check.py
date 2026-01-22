import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print(" ERROR: API Key not found. Check your .env file.")
else:
    print(f" API Key found: {api_key[:5]}...{api_key[-4:]}")

    client = OpenAI(api_key=api_key)

    try:
      
        print("Sending test request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API Connection Successful' in Ayurveda style."}],
            max_tokens=20
        )
        
        print("\n--- RESPONSE FROM AI ---")
        print(response.choices[0].message.content)
        print("------------------------")
        print("🎉 Your API is working perfectly!")

    except Exception as e:
        print(f"\nAPI CALL FAILED: {e}")