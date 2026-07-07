# Sherlock - Case File AI Assistant

A Retrieval Augmented Generation (RAG) system that allows detectives to upload case files and ask questions about suspects, alibis, and clues. Built with Python, Flask, FAISS, and Google AI.

## Features

- 📤 Upload case files (PDF or TXT)
- 🔍 Ask natural language questions
- 🎯 RAG-based answers (no hallucination)
- 🐳 Docker containerized
- 🎨 Modern web interface

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Google AI API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Setup

1. Clone and navigate to repository
```bash
git clone https://github.com/gellert4/project1.git
cd project1
```

2. Create `.env` file with your API key
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your GOOGLE_API_KEY
```

3. Build and run with Docker Compose
```bash
docker-compose up --build
```

4. Open browser to http://localhost:3000

## Local Development

### Prerequisites

- Python 3.10+
- pip and venv

### Setup

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r backend/requirements.txt

# Create .env with GOOGLE_API_KEY
cp backend/.env.example backend/.env
```

### Run Backend

```bash
cd backend
python app/main.py
```

Backend runs on http://localhost:5000

### Run Frontend

```bash
# In another terminal
cd frontend
# Serve static files (use any server, e.g., Python's built-in)
python -m http.server 3000
```

Frontend runs on http://localhost:3000

## Project Structure

```
sherlock/
├── backend/                 # Python API service
│   ├── app/
│   │   ├── main.py         # Flask API endpoints
│   │   └── rag/
│   │       ├── document_handler.py  # File upload & embedding
│   │       └── query_engine.py      # RAG query logic
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Web interface
│   ├── index.html
│   ├── script.js
│   └── style.css
├── nginx.conf              # Nginx reverse proxy config
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Upload Document
```
POST /api/documents
Content-Type: multipart/form-data
Body: file (PDF or TXT)

Response: { "success": true, "filename": "...", "chunks": 10 }
```

### List Documents
```
GET /api/documents

Response: { "documents": ["case1.txt", "case2.pdf"] }
```

### Query
```
POST /api/query
Content-Type: application/json
Body: { "question": "What was Mrs. Hudson's alibi?" }

Response: {
  "answer": "...",
  "sources": ["case1.txt"],
  "confidence": 0.85
}
```

## How RAG Works

1. **Document Upload** → Extract text, split into chunks
2. **Embedding** → Create vector embeddings using Sentence Transformers
3. **Store** → Save in FAISS vector database
4. **Query** → Find similar chunks using semantic search
5. **Generate** → LLM creates answer from context (no hallucination)

## Testing

```bash
# Test document handler locally
python test_document_handler.py
```

## Environment Variables

- `GOOGLE_API_KEY` - Your Google AI API key
- `FLASK_ENV` - development or production
- `DEBUG` - True/False

## Cost

Free tier usage:
- Google AI: 60 requests/minute (free)
- No GPU required
- ~100MB disk per 10k case documents

## Next Steps

- [ ] Add support for .docx files
- [ ] Implement user authentication
- [ ] Add case file metadata/tagging
- [ ] Implement multi-language support
- [ ] Add test suite

