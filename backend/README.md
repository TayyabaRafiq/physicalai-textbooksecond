---
title: Physical AI RAG Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Physical AI RAG Backend

FastAPI backend for the Physical AI textbook RAG chatbot.

## API Endpoints

- `GET /health` - Health check
- `POST /api/v1/ingest` - Ingest textbook content
- `POST /api/v1/question` - Ask questions about the textbook

## Environment Variables Required

Configure these in your Hugging Face Space settings (as Secrets):

- `COHERE_API_KEY` - Your Cohere API key
- `COHERE_MODEL_GENERATE` - Cohere model to use
- `QDRANT_API_KEY` - Your Qdrant Cloud API key
- `QDRANT_URL` - Your Qdrant Cloud URL
- `NEON_DATABASE_URL` - Your Neon Postgres connection string

## Documentation

Once deployed, visit:
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)
- `/health` - Health check endpoint

