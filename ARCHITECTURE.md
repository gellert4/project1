# Architecture

## Overview

```text
Frontend
   |
Flask REST API
   |
   +-- DocumentHandler
   |     - loads PDF/TXT
   |     - chunks text
   |     - creates embeddings
   |     - stores data in FAISS
   |
   +-- QueryEngine
         - retrieves relevant chunks
         - builds evidence context
         - calls Google Gemini
```

## Components

### Frontend

HTML, CSS and JavaScript provide file upload, question input, answer display, sources and document listing.

### Backend

The Flask API exposes:

```text
POST /api/documents
GET  /api/documents
POST /api/query
GET  /health
```

### Retrieval

Sentence Transformer embeddings are stored in FAISS and searched for each question.

### Deployment

Docker Compose starts the Flask backend and the Nginx-served frontend.
