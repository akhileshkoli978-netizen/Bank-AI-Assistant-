🏦 Bank AI Assistant

An AI-powered banking query assistant built as a college project using Base44 + FastAPI + Google Gemini + Render.






🌐 Live Demo

👉 https://bank-smart-chat.base44.app/

The frontend is hosted through Base44 and communicates with the FastAPI backend deployed on Render.

Backend: https://bank-ai-assistant-wtxb.onrender.com/

API Documentation: https://bank-ai-assistant-wtxb.onrender.com/docs

⚠️ This is an educational/demo project. It is not connected to real bank accounts and cannot perform real banking transactions.

📌 Project Overview

Bank AI Assistant is a conversational banking assistant designed to answer general banking questions using:

A local banking FAQ knowledge base

FAQ retrieval based on keyword relevance

Google Gemini for AI-generated responses

FastAPI REST API

Base44 frontend

Render cloud deployment

The project demonstrates how an AI assistant can be connected to a custom knowledge base and exposed through a web interface.

✨ Features

🤖 AI-powered banking Q&A

🏦 Banking-focused knowledge base

🔎 FAQ retrieval

🧠 Google Gemini integration

🔄 Gemini fallback handling

🛡️ Banking safety rules

🌐 REST API using FastAPI

🎨 Modern Base44 chat interface

☁️ Render deployment

📱 Responsive frontend

⚡ Local FAQ fallback when AI generation is unavailable

📚 FastAPI Swagger documentation

🏗️ System Architecture

                         ┌──────────────────────┐
                         │     Base44 Frontend  │
                         │   Banking Chat UI    │
                         └──────────┬───────────┘
                                    │
                                    │ POST /chat
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         │       Render         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    src/chatbot.py    │
                         └───────┬───────┬──────┘
                                 │       │
                    ┌────────────┘       └────────────┐
                    ▼                                 ▼
          ┌──────────────────┐              ┌─────────────────┐
          │ banking_faq.txt  │              │   Gemini API    │
          │ Knowledge Base   │              │ AI Generation   │
          └──────────────────┘              └─────────────────┘

🔄 How It Works

User asks a question
        ↓
Base44 Chat Interface
        ↓
POST /chat
        ↓
FastAPI Backend
        ↓
FAQ Retrieval
        ↓
Relevant FAQ Context
        ↓
Gemini AI Prompt
        ↓
AI-generated Answer
        ↓
Base44 displays answer

If Gemini is unavailable:

Gemini Error / Quota
        ↓
Try fallback model
        ↓
If generation still fails
        ↓
Local FAQ fallback
        ↓
Return useful response

🧰 Technologies Used

Technology

Purpose

Python

Backend programming

FastAPI

REST API framework

Uvicorn

ASGI server

Google Gemini API

AI response generation

Google GenAI SDK

Gemini integration

Base44

Frontend / UI

Render

Cloud backend deployment

GitHub

Source-code management

banking_faq.txt

Banking knowledge base

dotenv

Environment configuration

📂 Project Structure

Bank-AI-Assistant/
│
├── api.py
├── requirements.txt
├── README.md
│
├── src/
│   └── chatbot.py
│
├── data/
│   └── banking_faq.txt
│
└── .env

Do not commit .env if it contains a real Gemini API key.

🤖 AI & FAQ Retrieval Method

The chatbot uses the local FAQ file as its knowledge source.

For every user question, the backend:

Loads the banking FAQ knowledge base.

Splits the FAQ content into manageable chunks.

Tokenizes the user's question.

Removes common stopwords.

Calculates keyword overlap with FAQ chunks.

Applies phrase matching/relevance scoring.

Selects relevant FAQ content.

Adds the retrieved context to the Gemini prompt.

Generates a concise banking response.

This approach keeps the application lightweight and suitable for deployment without requiring a separate vector database.

🧠 Gemini AI Integration

The main configured model is:

gemini-3.8-flash

Fallback models can include:

gemini-3.7-flash
gemini-3.6-flash
gemini-3.5-flash-lite

The backend is designed to handle common Gemini API failures such as:

429 RESOURCE_EXHAUSTED
404 NOT_FOUND
503 UNAVAILABLE
500 / 504 temporary errors

Temporary availability errors can be retried using exponential backoff.

If AI generation cannot be completed, the application falls back to the local FAQ knowledge base.

📉 Gemini Quota Handling

Gemini API usage is subject to project/model quotas.

A typical quota error looks like:

429 RESOURCE_EXHAUSTED

The application handles this by avoiding unnecessary retries of an exhausted model and moving to configured fallback models.

The final fallback is the local FAQ system.

Primary Gemini Model
        │
        ├── Success ──────► AI Answer
        │
        └── Error
              ↓
       Fallback Gemini Model
              │
              ├── Success ─► AI Answer
              │
              └── Error
                    ↓
              Local FAQ Answer

This makes the demo more resilient when Gemini quota or model availability becomes an issue.

🎨 Base44 Frontend

The Base44 application provides the user-facing banking assistant interface.

UI Goals

The interface was designed around a:

Premium banking/fintech aesthetic

Futuristic AI feel

Dark visual theme

Glassmorphism-style cards

Banking-focused chat experience

Responsive layout

Lightweight animations

The UI concept includes:

Deep black/dark background

Navy, cyan, teal and electric-blue visual accents

Glass-style interface elements

Mouse-following glow effects

Ambient/gradient lighting

AI thinking animation

"Assistant is thinking..." indicator

Banking-style chat cards

Responsive behavior

Reduced-motion consideration

The animations should remain lightweight and should not interfere with the banking chat functionality.

📝 Base44 Prompts Used

1. Base44 API Connection Prompt

The Base44 frontend was configured to communicate with the deployed backend using:

POST https://bank-ai-assistant-wtxb.onrender.com/chat

Request:

{
  "question": "USER_QUESTION"
}

The frontend reads the returned:

{
  "answer": "..."
}

and displays the answer value to the user.

The frontend should:

Send the user's question to /chat.

Wait for the backend response.

Read response.json().answer.

Display the returned answer.

Show a loading state while waiting.

Show a friendly error state if the request fails.

Preserve the existing UI.

Keep the Gemini API key completely out of the frontend.

2. Base44 UI Interface Prompt

The UI redesign direction was:

“Redesign the existing Bank AI Assistant interface to have a premium, futuristic banking/fintech aesthetic.”

Important requirements:

Preserve existing API/backend/chat logic.

Use a deep black background.

Use navy/cyan/teal/electric-blue accents.

Use glassmorphism.

Add a mouse-following glow.

Add animated gradient/ambient lighting while AI is thinking.

Display an "Assistant is thinking..." indicator.

Return to the normal dark background after the answer arrives.

Use banking-style chat cards.

Keep the interface responsive.

Support reduced-motion preferences.

Keep animations lightweight.

3. Base44 Connection-Fix Prompt

The frontend connection was configured so that:

HTTP 200 with JSON containing an answer field is treated as a successful response.

The exact value of response.json().answer is displayed.

The frontend does not require a Gemini API key.

Gemini credentials are never exposed in Base44.

Existing UI design is preserved.

🛡️ Banking Safety

The assistant must never ask users for sensitive banking credentials.

Never request or expose:

❌ OTP

❌ PIN

❌ CVV

❌ Passwords

❌ Passcodes

❌ Full card numbers

❌ Account passwords

❌ Banking credentials

The assistant also:

Does not perform real banking transactions.

Does not claim to perform transactions.

Does not guarantee loan approval.

Does not guarantee investment returns.

Does not guarantee product suitability.

Does not invent current bank-specific rates.

Does not invent fees, limits, offers or eligibility rules.

Recommends checking official bank sources for current information.

⚙️ API

GET /

Health-check endpoint.

Example:

{
  "status": "online",
  "message": "Bank AI Assistant API is running"
}

POST /chat

Main chatbot endpoint.

Request:

{
  "question": "What is KYC?"
}

Response:

{
  "answer": "KYC stands for Know Your Customer. It is a customer verification process used by financial institutions to verify customer identity and other required information."
}

Swagger Documentation

https://bank-ai-assistant-wtxb.onrender.com/docs

☁️ Render Deployment

The FastAPI backend is deployed on Render.

Build Command

pip install -r requirements.txt

Start Command

uvicorn api:app --host 0.0.0.0 --port $PORT

Environment Variables

Configure these in Render:

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash

The real API key should only exist in the server environment.

🔐 Security

The Gemini API key must never be placed inside:

Base44 frontend code

GitHub source files

README files

Screenshots

Client-side JavaScript

Public configuration

Use environment variables instead:

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash

If an API key is accidentally exposed, revoke/rotate it immediately.

🧪 Example Questions

Try questions such as:

What is KYC?
What is a savings account?
What is a credit card?
What is a fixed deposit?
What is a loan?
Can an AI assistant recommend a loan?
Should I share my OTP with a chatbot?
Can a chatbot perform a bank transaction?
What information can be used for a basic product recommendation?

🚫 Project Limitations

This project is for educational and demonstration purposes.

It does not:

Connect to real bank accounts.

Read real account balances.

Transfer money.

Make payments.

Perform account operations.

Verify real customer identity.

Execute real banking transactions.

Guarantee financial decisions.

Replace official bank support.

Guarantee current bank-specific rates or fees.

🔧 Local Installation

1. Clone the repository

git clone https://github.com/<your-username>/Bank-AI-Assistant.git
cd Bank-AI-Assistant

2. Create a virtual environment

Windows

python -m venv .venv
.venv\Scriptsctivate

macOS/Linux

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create .env:

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash

5. Run the API

uvicorn api:app --reload

Open:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

🔗 Project Links

Resource

Link

🌐 Live Frontend

https://bank-smart-chat.base44.app/

🚀 Render Backend

https://bank-ai-assistant-wtxb.onrender.com/

📚 API Documentation

https://bank-ai-assistant-wtxb.onrender.com/docs

🎓 College Project Information

Project Name: Bank AI Assistant

Project Type: AI / Banking / Web Application

Purpose: Demonstrate how an AI-powered conversational assistant can be integrated with a custom banking knowledge base and deployed as a web application.

Concepts Demonstrated

Artificial Intelligence

Generative AI

Prompt Engineering

FAQ Retrieval

REST API Development

FastAPI

Frontend/Backend Integration

Cloud Deployment

Gemini API Integration

Error Handling

AI Safety

Secure Environment Variables

📸 Screenshots

Add screenshots of your application here after taking them from the live Base44 interface.

Example:

![Bank AI Assistant Home Screen](screenshots/home.png)

![Bank AI Assistant Chat](screenshots/chat.png)

Recommended screenshots:

Home screen

Chat screen

Example banking question

AI response

Render API /docs

GitHub repository

🧩 Future Improvements

Possible future improvements include:

User authentication for a simulated demo environment

Better semantic/vector search

Larger banking knowledge base

Multi-language support

Voice input/output

Conversation history

Improved analytics

More detailed banking product comparisons

Better monitoring and logging

Additional AI models

Automated testing

Any future implementation should continue to follow the project's banking safety rules.

📜 Disclaimer

This project is created for educational and demonstration purposes only.

It is not affiliated with, operated by, or endorsed by any real bank.

The assistant should not be used as a substitute for official financial or banking advice.

For current and bank-specific information, always verify details through the relevant bank's official channels.

⭐ Demo

🚀 Try the Bank AI Assistant

https://bank-smart-chat.base44.app/

If you find the project useful, consider giving the repository a ⭐.
