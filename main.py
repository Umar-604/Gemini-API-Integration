import google.generativeai as genai
from config import GEMINI_API_KEY
from database import init_db, save_chat

init_db()  # Initialize DB only once

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Use the best available Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        gemini_response = response.text

        save_chat(prompt, gemini_response)  # ✅ Save after generation
        return gemini_response

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("🧬 Welcome to Gemini Chat. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        print("Gemini:", ask_gemini(user_input))
