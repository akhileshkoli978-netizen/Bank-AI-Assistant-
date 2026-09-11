# 🏦 Bank AI Assistant

An AI-powered banking assistant that answers general banking questions using a local banking knowledge base, ChromaDB vector search, and Gemini.

## Architecture

```text
Base44 Frontend
      |
      | POST /chat
      v
FastAPI (api.py)
      |
      v
src/chatbot.py
      |
      +--> ChromaDB
      |
      +--> Gemini
```

## Features

- AI-powered banking chatbot
- Natural-language questions
- Banking FAQ retrieval
- ChromaDB vector search
- Gemini-powered answers
- FastAPI backend for external frontends such as Base44
- Safe fallback when AI generation is unavailable
- Does not perform real banking transactions

## Project Structure

```text
Bank-AI-Assistant/
├── api.py
├── app.py
├── requirements.txt
├── render.yaml
├── .gitignore
├── .env.example
├── data/
│   └── banking_faq.txt
├── src/
│   ├── chatbot.py
│   └── load_data.py
└── database/
    └── chroma_db/
```

## Local Setup

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env`

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Never upload `.env` to GitHub.**

### 4. Build the ChromaDB knowledge base

Run this once:

```bash
python src/load_data.py
```

This reads `data/banking_faq.txt` and creates the local ChromaDB collection.

### 5. Test the Streamlit application

```bash
streamlit run app.py
```

### 6. Run the FastAPI backend

```bash
uvicorn api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Chat endpoint:

```text
POST http://127.0.0.1:8000/chat
```

Example request:

```json
{
  "question": "What is a savings account?"
}
```

Example response:

```json
{
  "answer": "..."
}
```

## Base44 Integration

After deploying the FastAPI backend, use the public HTTPS backend URL in Base44.

For example:

```text
https://YOUR-BACKEND.onrender.com/chat
```

Configure Base44 to send:

```http
POST /chat
Content-Type: application/json
```

with:

```json
{
  "question": "What is UPI?"
}
```

The backend returns:

```json
{
  "answer": "..."
}
```

## Deployment

The included `render.yaml` is prepared for a Render web service.

The required environment variable is:

```text
GEMINI_API_KEY
```

Set it in the deployment platform's environment-variable settings. Do not commit the key.

## Safety

This is an educational project. It does not connect to real bank accounts and does not perform banking transactions.

Users should never provide passwords, PINs, OTPs, CVVs, full card numbers, or other sensitive banking credentials.

Current bank-specific rates, fees, limits, and policies should be verified with the relevant bank.

## License

Educational / academic project.
