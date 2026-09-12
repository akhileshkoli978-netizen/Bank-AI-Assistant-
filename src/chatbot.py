import os
import re
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "banking_faq.txt"

load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use a current Gemini model. You can override it in Render without changing code.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "can", "do", "does", "for",
    "from", "how", "i", "in", "is", "it", "me", "my", "of", "on", "or",
    "the", "to", "what", "when", "where", "which", "with", "you", "your",
}

_SAFETY_TERMS = {
    "otp", "pin", "cvv", "password", "passcode", "card number",
    "account number", "credentials",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}


@lru_cache(maxsize=1)
def _faq_chunks() -> tuple[str, ...]:
    """Load and chunk the FAQ once per process.

    This intentionally avoids requiring a pre-built Chroma database on Render.
    The repository's banking_faq.txt remains the single source of knowledge.
    """
    if not DATA_FILE.exists():
        return ()

    text = DATA_FILE.read_text(encoding="utf-8")
    raw_chunks = re.split(r"\n(?=Q:\s)", text)

    chunks: list[str] = []
    for chunk in raw_chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        # Keep chunks reasonably small for the prompt.
        if len(chunk) <= 1800:
            chunks.append(chunk)
        else:
            for start in range(0, len(chunk), 1600):
                part = chunk[start:start + 1800].strip()
                if part:
                    chunks.append(part)
    return tuple(chunks)


def _retrieve(question: str, k: int = 4) -> list[str]:
    chunks = _faq_chunks()
    if not chunks:
        return []

    q_tokens = _tokens(question)
    if not q_tokens:
        return list(chunks[:k])

    scored = []
    q_lower = question.lower()

    for index, chunk in enumerate(chunks):
        c_tokens = _tokens(chunk)
        overlap = len(q_tokens & c_tokens)
        phrase_bonus = 2 if q_lower in chunk.lower() else 0
        score = overlap + phrase_bonus

        if score > 0:
            scored.append((score, -index, chunk))

    scored.sort(reverse=True)
    return [chunk for _, _, chunk in scored[:k]]


def _fallback_answer(results: list[str]) -> str:
    if not results:
        return (
            "Sorry, I could not find relevant information in the banking "
            "knowledge base."
        )

    return (
        "⚠️ The AI generation service is temporarily unavailable.\n\n"
        "Here is the relevant information available in the banking "
        "knowledge base:\n\n" + "\n\n".join(results)
    )


@lru_cache(maxsize=1)
def _gemini_client():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured on the server."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def ask_banking_assistant(question: str) -> str:
    question = question.strip()
    if not question:
        return "Please enter a banking question."

    results = _retrieve(question)

    # Never send credentials back to the model or request them.
    lowered = question.lower()
    if any(term in lowered for term in _SAFETY_TERMS):
        # The model can answer general safety questions, but the prompt
        # explicitly prevents requesting sensitive information.
        pass

    context = "\n\n".join(results)
    if not context:
        context = (
            "No matching entry was found in the current banking knowledge base."
        )

    prompt = f"""
You are the AI Banking Query Assistant for a college project.

Answer the user's question using ONLY the banking knowledge provided below.

Rules:
1. Do not invent banking information.
2. Do not invent current interest rates, fees, eligibility rules, policies,
   limits, or offers.
3. If the answer is not in the knowledge base, say that clearly.
4. Never ask the user for an OTP, PIN, CVV, password, full card number,
   account password, or other sensitive banking credentials.
5. Do not perform or claim to perform real banking transactions.
6. For bank-specific or current information, tell the user to verify it
   with the relevant bank's official channel.
7. Keep the answer concise and easy to understand.

BANKING KNOWLEDGE:
------------------
{context}
------------------

USER QUESTION:
{question}

Answer:
""".strip()

    try:
        client = _gemini_client()

        # This is the supported Google GenAI Python SDK pattern.
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        answer = getattr(response, "text", None)
        if answer:
            return answer.strip()

        return _fallback_answer(results)

    except Exception as exc:
    import logging
    logging.exception("Gemini API request failed: %s", exc)
    return _fallback_answer(results)

if __name__ == "__main__":
    print(ask_banking_assistant(input("Ask your banking question: ")))
