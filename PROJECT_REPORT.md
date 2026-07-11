# Sherlock – Final Report

## Overview

Sherlock is a Retrieval Augmented Generation application that allows users to upload PDF or TXT case files and ask questions about their contents.

## Implementation

The Flask backend provides endpoints for uploading documents, listing uploaded files, asking questions and checking service health.

Documents are parsed, split into chunks, embedded with Sentence Transformers and stored in FAISS. For each question, the most relevant chunks are retrieved and sent to Google Gemini as evidence. The prompt instructs the model to answer only from that evidence and to return an insufficient-evidence response when necessary.

The frontend is implemented with HTML, CSS and JavaScript.

## Architecture

```text
Frontend
   |
Flask REST API
   |
Document processing
   |
Sentence Transformer embeddings
   |
FAISS retrieval
   |
Google Gemini
```

## Technology choices

- Flask for a lightweight REST API
- FAISS for local vector search
- Sentence Transformers for free local embeddings
- Google Gemini for natural-language answers
- Docker Compose for reproducible startup
- Vanilla JavaScript for a simple frontend

## Limitations

- Local FAISS storage is intended for a single-user prototype
- Free-tier LLM availability can occasionally cause temporary errors
- Retrieval confidence is simplified and not a calibrated probability
- Authentication and production persistence are outside the task scope

## Result

The project provides the required Python API, document upload, RAG retrieval, LLM-generated answers, frontend and Docker setup.
