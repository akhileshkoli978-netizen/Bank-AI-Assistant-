import os

from dotenv import load_dotenv
from google import genai


# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )


# Create Gemini client
client = genai.Client(api_key=api_key)


# Send a test request using the current Interactions API
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="What is a savings account? Explain in two simple sentences."
)


print("\n========== GEMINI RESPONSE ==========\n")
print(interaction.output_text)