# Sherlock

Sherlock is a small Retrieval Augmented Generation (RAG) application for uploading PDF or TXT case files and asking questions about their contents.

The system retrieves relevant document chunks from a FAISS vector store and sends only that evidence to Google Gemini. If the evidence is insufficient, the expected response is:

> I don't have enough evidence to answer that.

## Features

- Upload PDF and TXT case files
- Ask natural-language questions
- Semantic retrieval with Sentence Transformers and FAISS
- Evidence-grounded answers with Google Gemini
- REST API built with Flask
- Simple browser frontend
- Docker and Docker Compose support

## Tech stack

- Python 3.10+
- Flask
- LangChain
- Sentence Transformers
- FAISS
- Google Gen AI SDK
- HTML, CSS and JavaScript
- Nginx
- Docker Compose

## Setup

### Docker

Create `backend/.env`:

```env
GOOGLE_API_KEY=your_google_ai_api_key
FLASK_ENV=development
DEBUG=True
```

Then run:

```bash
docker compose up --build
```

Open `http://localhost:3000`.

### Local development

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
python run.py
```

In a second terminal:

```powershell
cd frontend
python -m http.server 3000
```

## API

- `POST /api/documents`
- `GET /api/documents`
- `POST /api/query`
- `GET /health`

## Testing

```bash
pytest -v
```

## Notes

- Do not commit `.env`, uploaded files or generated FAISS data.
- Gemini free-tier availability may occasionally cause temporary errors.
- This is a coding-test prototype, not a production deployment.

## Configuration

Create a `.env` file inside the `backend` directory:

```env
GOOGLE_API_KEY=YOUR_GOOGLE_AI_API_KEY
FLASK_ENV=development
DEBUG=True
```

A free API key can be obtained from Google AI Studio:
https://aistudio.google.com/app/apikey
