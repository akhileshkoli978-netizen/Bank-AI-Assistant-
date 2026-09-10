import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# Project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"
DATABASE_DIR = BASE_DIR / "database" / "chroma_db"


# ============================================================
# Load environment variables
# ============================================================

load_dotenv(ENV_FILE)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )


# ============================================================
# Load Gemini client once
# ============================================================

@st.cache_resource
def get_gemini_client():

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# Load embedding model once
# ============================================================

@st.cache_resource
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ============================================================
# Load ChromaDB once
# ============================================================

@st.cache_resource
def get_vector_store():

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name="banking_knowledge",
        embedding_function=embeddings,
        persist_directory=str(DATABASE_DIR)
    )

    return vector_store


# ============================================================
# Search local banking knowledge
# ============================================================

def search_banking_knowledge(question: str):

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        question,
        k=3
    )

    return results


# ============================================================
# Create fallback answer
# ============================================================

def create_fallback_answer(results):

    if not results:

        return (
            "Sorry, I could not find relevant information "
            "in the banking knowledge base."
        )

    information = []

    for document in results:

        information.append(
            document.page_content
        )

    answer = (
        "⚠️ The AI generation service is temporarily "
        "unavailable.\n\n"
        "Here is the relevant information available "
        "in the banking knowledge base:\n\n"
    )

    answer += "\n\n".join(information)

    return answer


# ============================================================
# Main Banking Assistant
# ============================================================

def ask_banking_assistant(question: str):

    # --------------------------------------------------------
    # 1. Search local knowledge base
    # --------------------------------------------------------

    results = search_banking_knowledge(question)


    # --------------------------------------------------------
    # 2. Create context
    # --------------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in results
    )


    # --------------------------------------------------------
    # 3. Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI Banking Query Assistant for a college project.

Answer the user's question using the banking knowledge
provided below.

IMPORTANT RULES:

1. Use the provided banking context.
2. Do not invent banking information.
3. Do not invent interest rates, fees, eligibility,
   policies, or other financial details.
4. If the answer is not available in the context,
   clearly say that it is not available in the current
   banking knowledge base.
5. Do not perform banking transactions.
6. Never ask for passwords, PINs, OTPs, CVV, account
   numbers, or other sensitive banking credentials.
7. Keep the answer simple and easy to understand.

BANKING KNOWLEDGE:
------------------
{context}
------------------

USER QUESTION:
{question}

Provide a concise answer based only on the banking knowledge.
"""


    # --------------------------------------------------------
    # 4. Try Gemini
    # --------------------------------------------------------

    try:

        client = get_gemini_client()

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return interaction.output_text


    # --------------------------------------------------------
    # 5. Gemini quota / API failure
    # --------------------------------------------------------

    except Exception as e:

        error_message = str(e).lower()

        if (
            "quota" in error_message
            or "429" in error_message
            or "rate" in error_message
            or "too_many_requests" in error_message
        ):

            return create_fallback_answer(results)

        # Other API errors also get a safe fallback
        return create_fallback_answer(results)


# ============================================================
# Terminal testing
# ============================================================

if __name__ == "__main__":

    question = input(
        "Ask your banking question: "
    )

    answer = ask_banking_assistant(question)

    print(
        "\n========== BANK AI ASSISTANT ==========\n"
    )

    print(answer)