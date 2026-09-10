import os

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )


# Gemini client
client = genai.Client(
    api_key=api_key
)


# Ask a question that needs current web information
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=(
        "What documents are generally required to open "
        "a savings account at HDFC Bank? "
        "Use current web information and prefer official "
        "HDFC Bank sources."
    ),
    tools=[
        {
            "type": "google_search"
        }
    ]
)


print("\n========== GEMINI WEB RESPONSE ==========\n")

print(interaction.output_text)


# Print citations
print("\n========== SOURCES ==========\n")

for step in interaction.steps:

    if step.type == "model_output":

        for content_block in step.content:

            if (
                content_block.type == "text"
                and content_block.annotations
            ):

                for annotation in content_block.annotations:

                    if annotation.type == "url_citation":

                        print(
                            f"{annotation.title}: "
                            f"{annotation.url}"
                        )