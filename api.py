from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.chatbot import ask_banking_assistant

app = FastAPI(
    title="Bank AI Assistant API",
    description="API for the Bank AI Assistant college project.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Bank AI Assistant API is running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = ask_banking_assistant(request.question)
        return {"answer": answer}
    except Exception as exc:
        # Do not expose API keys or internal stack traces to the client.
        raise HTTPException(
            status_code=500,
            detail="The banking assistant could not process the request.",
        ) from exc
