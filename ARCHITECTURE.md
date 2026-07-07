# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│  - File upload interface                                     │
│  - Question input form                                       │
│  - Results display                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       │
    ┌──────────────────▼──────────────────┐
    │         NGINX REVERSE PROXY          │
    │  - Routing (/api → backend)          │
    │  - CORS headers                      │
    │  - Static file serving               │
    └──────────────────┬──────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      FLASK API                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Endpoints:                                             │ │
│  │ - POST /api/documents (upload case files)              │ │
│  │ - GET /api/documents (list uploaded files)             │ │
│  │ - POST /api/query (ask questions)                      │ │
│  │ - GET /health (health check)                           │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐          ┌────────▼──────────┐
│ DocumentHandler│          │  QueryEngine      │
│ - Extract text │          │ - RAG Logic       │
│ - Split chunks │          │ - LLM Integration │
│ - Embeddings   │          │ - Answer Gen      │
└───────┬────────┘          └────────┬──────────┘
        │                            │
        └────────────┬───────────────┘
                     │
        ┌────────────▼──────────────┐
        │  FAISS Vector Database    │
        │ - Store embeddings        │
        │ - Similarity search       │
        │ - Fast retrieval          │
        └───────────────────────────┘
```

## Components

### Frontend
- HTML/CSS/JavaScript
- No build step (served directly by Nginx)
- Dynamic API calls
- Real-time status updates

### Backend
- Flask REST API
- Python 3.10+
- Modular architecture

#### Document Handler
- Processes PDF/TXT files
- Splits into chunks (500 chars, 50 overlap)
- Creates embeddings using Sentence Transformers (all-MiniLM-L6-v2)
- Stores in FAISS vector database

#### Query Engine
- Semantic search (finds top-3 similar chunks)
- Context preparation
- LLM integration (Google AI Gemini)
- Hallucination detection
- Fallback mode (without LLM)

### Infrastructure
- Docker for containerization
- Docker Compose for orchestration
- Nginx for routing and reverse proxy
- FAISS for vector storage (CPU-based)

## Data Flow

### Upload Case File
```
User Upload
    ↓
File Upload Endpoint
    ↓
Extract Text (PDF/TXT)
    ↓
Split into Chunks
    ↓
Create Embeddings (Sentence Transformers)
    ↓
Store in FAISS DB
    ↓
Return success response
```

### Query
```
User Question
    ↓
Search Vector DB (semantic)
    ↓
Retrieve Top-3 Similar Chunks
    ↓
Prepare Context
    ↓
Generate Answer (LLM)
    ↓
Validate (no hallucination)
    ↓
Return Answer + Sources
```

## Technology Choices

| Component | Technology | Why |
|-----------|-----------|-----|
| Backend | Flask | Lightweight, Python ecosystem |
| Vector DB | FAISS | Fast similarity search, CPU-based |
| Embeddings | Sentence Transformers | Small, accurate, open-source |
| LLM | Google AI Gemini | Free tier, good API |
| Frontend | Vanilla JS | No build step, simple |
| Reverse Proxy | Nginx | Lightweight, fast, CORS support |
| Container | Docker | Reproducible, portable |

## Security Considerations

- Input validation on all endpoints
- File type validation (PDF/TXT only)
- File size limits (50MB max)
- No direct database exposure
- CORS headers configured
- API key management via env variables

## Scalability

Current design can handle:
- ~1000 case files per instance
- ~100k queries per day (within free tier)
- Latency: ~500ms average query

Future improvements:
- Add caching layer (Redis)
- Implement database persistence
- Load balancing for multiple backends
- Better vector DB (Pinecone, Weaviate)
