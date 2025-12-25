# Quickstart Guide: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend – Core Question Answering Pipeline
**Date**: 2025-12-21
**Audience**: Backend developers setting up the development environment

## Overview

This guide walks you through setting up the RAG chatbot backend development environment from scratch. By the end, you'll have a running local instance that can ingest textbook content and answer questions.

---

## Prerequisites

### Required Software

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Docker** (optional, for containerized deployment) - [Download](https://www.docker.com/products/docker-desktop)

### Required Accounts & API Keys

1. **Cohere API Key**
   - Sign up at https://cohere.com
   - Navigate to API Keys section
   - Create a new API key (free tier: 1000 calls/month)

2. **Qdrant Cloud**
   - Sign up at https://cloud.qdrant.io
   - Create a new cluster (free tier: 1GB storage)
   - Note the cluster URL and API key

3. **Neon Serverless Postgres**
   - Sign up at https://neon.tech
   - Create a new project
   - Copy the connection string (looks like `postgresql://user:password@host/database`)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/ai-textbook.git
cd ai-textbook/backend
```

---

## Step 2: Set Up Python Environment

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
# Install all dependencies from pyproject.toml
pip install -e ".[dev]"

# Or if using requirements.txt:
pip install -r requirements.txt
```

**Core Dependencies** (defined in `pyproject.toml`):
- `fastapi>=0.104.0` - Web framework
- `uvicorn[standard]>=0.24.0` - ASGI server
- `cohere>=4.0.0` - Cohere SDK
- `qdrant-client>=1.7.0` - Qdrant client
- `sqlalchemy>=2.0.0` - PostgreSQL ORM
- `asyncpg>=0.29.0` - Async Postgres driver
- `pydantic>=2.0.0` - Data validation
- `python-dotenv>=1.0.0` - Environment variables
- `alembic>=1.12.0` - Database migrations
- `slowapi>=0.1.9` - Rate limiting

**Dev Dependencies**:
- `pytest>=7.4.0`
- `pytest-asyncio>=0.21.0`
- `httpx>=0.25.0` - Async HTTP client for testing
- `pytest-cov>=4.1.0` - Code coverage

---

## Step 3: Configure Environment Variables

### Create `.env` File

Copy the `.env.example` template:

```bash
cp .env.example .env
```

### Fill in API Keys

Edit `.env` with your actual credentials:

```env
# Cohere API Configuration
COHERE_API_KEY=your-cohere-api-key-here

# Qdrant Cloud Configuration
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_CLUSTER_ID=your-cluster-id

# Neon Serverless Postgres Configuration
NEON_DATABASE_URL=postgresql://user:password@host/database

# Application Configuration (optional)
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_RATE_LIMIT_INGESTION=10  # requests/minute
API_RATE_LIMIT_QUESTIONS=100  # requests/minute
```

**⚠️ Security**: NEVER commit `.env` to version control. The `.gitignore` file already excludes it.

---

## Step 4: Initialize Database Schema

### Run Alembic Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Generate initial migration (or use existing migration)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations to Neon database
alembic upgrade head
```

This creates the following tables in Neon Postgres:
- `modules`
- `chapters`
- `sections`
- `chunks`
- `question_log`
- `answer_log`

### Initialize Qdrant Collection

```bash
# Run the initialization script
python -m src.scripts.init_qdrant
```

This creates the `textbook_chunks` collection in Qdrant Cloud with:
- Vector size: 1024 (Cohere embed-english-v3.0)
- Distance metric: Cosine similarity

---

## Step 5: Start the Development Server

### Run with Uvicorn

```bash
# Start server with hot reload
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verify Server is Running

Open your browser and navigate to:

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

You should see the OpenAPI documentation and be able to test endpoints interactively.

---

## Step 6: Ingest Sample Content

### Prepare Sample Markdown File

Create a sample textbook module file at `content/sample-module.md`:

```markdown
# Module 1: Introduction to Physical AI

This module introduces the fundamental concepts of Physical AI.

## Chapter 1: What is Physical AI?

Physical AI refers to artificial intelligence systems that interact with the physical world.

### Section 1.1: Defining Physical AI

Physical AI combines perception, reasoning, and action in embodied agents like robots.
These systems operate in real-world environments, unlike purely digital AI systems.

### Section 1.2: Key Characteristics

Physical AI systems have three key characteristics:
1. Embodiment: They have physical form (robots, drones, etc.)
2. Perception: They sense the environment (cameras, sensors)
3. Action: They physically interact with the world (grippers, wheels, etc.)
```

### Submit Ingestion Request

Use the Swagger UI at http://localhost:8000/docs or curl:

```bash
curl -X POST "http://localhost:8000/api/v1/ingestion" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "content/sample-module.md",
    "module_title": "Module 1: Introduction to Physical AI",
    "module_description": "Foundational concepts in Physical AI",
    "module_order": 1
  }'
```

**Response**:
```json
{
  "job_id": "ing-123e4567-e89b-12d3-a456-426614174000",
  "status": "accepted",
  "message": "Ingestion job accepted. Check /api/v1/ingestion/status/ing-123e4567-e89b-12d3-a456-426614174000 for progress."
}
```

### Check Ingestion Status

```bash
curl "http://localhost:8000/api/v1/ingestion/status/ing-123e4567-e89b-12d3-a456-426614174000"
```

**Response** (when completed):
```json
{
  "job_id": "ing-123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "message": "Ingestion completed successfully",
  "progress": {
    "total_chunks": 3,
    "processed_chunks": 3,
    "percentage": 100
  }
}
```

---

## Step 7: Ask Questions

### Full Textbook Mode

Ask a question using the full textbook content:

```bash
curl -X POST "http://localhost:8000/api/v1/question" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is physical AI?"
  }'
```

**Response**:
```json
{
  "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents like robots. These systems combine perception, reasoning, and action to operate in real-world environments.",
  "sources": [
    {
      "module": "Module 1: Introduction to Physical AI",
      "chapter": "Chapter 1: What is Physical AI?",
      "section": "Section 1.1: Defining Physical AI",
      "chunk_id": 1
    }
  ],
  "mode": "full_textbook",
  "confidence": "high"
}
```

### Selected Text Mode

Ask a question about selected text:

```bash
curl -X POST "http://localhost:8000/api/v1/question/selected-text" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the three characteristics mentioned?",
    "selected_text": "Physical AI systems have three key characteristics: 1. Embodiment: They have physical form (robots, drones, etc.) 2. Perception: They sense the environment (cameras, sensors) 3. Action: They physically interact with the world (grippers, wheels, etc.)"
  }'
```

**Response**:
```json
{
  "answer": "The three key characteristics are: 1. Embodiment (physical form like robots or drones), 2. Perception (sensing the environment through cameras and sensors), and 3. Action (physically interacting with the world using grippers, wheels, etc.).",
  "sources": [],
  "mode": "selected_text",
  "confidence": "high"
}
```

---

## Step 8: Run Tests

### Run All Tests

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html

# Run specific test files
pytest tests/unit/test_chunker.py
pytest tests/integration/test_question_api.py
```

### View Coverage Report

```bash
# Open HTML coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

---

## Troubleshooting

### Common Issues

#### 1. "Connection refused" to Qdrant/Neon

**Problem**: Cannot connect to Qdrant or Neon databases.

**Solution**:
- Verify API keys and URLs in `.env` are correct
- Check Qdrant cluster is running (log into Qdrant Cloud dashboard)
- Test Neon connection: `psql $NEON_DATABASE_URL`

#### 2. "Rate limit exceeded" from Cohere

**Problem**: Too many API calls to Cohere (free tier: 1000/month).

**Solution**:
- Reduce test volume or use mocked Cohere client for unit tests
- Upgrade to Cohere paid tier if needed

#### 3. "Module not found" errors

**Problem**: Python cannot find `src` module.

**Solution**:
- Ensure you're in the `backend/` directory
- Reinstall in editable mode: `pip install -e .`
- Verify virtual environment is activated

#### 4. Alembic migration errors

**Problem**: "Target database is not up to date" or migration conflicts.

**Solution**:
- Check current migration state: `alembic current`
- Rollback and reapply: `alembic downgrade base && alembic upgrade head`
- If schema is corrupted, drop all tables and re-migrate (⚠️ destroys data)

---

## Next Steps

1. **Read the Specification** - See `specs/001-rag-chatbot-pipeline/spec.md`
2. **Review Data Model** - See `specs/001-rag-chatbot-pipeline/data-model.md`
3. **Explore API Contract** - See `specs/001-rag-chatbot-pipeline/contracts/openapi.yaml`
4. **Run Implementation Tasks** - Use `/sp.tasks` to generate task breakdown
5. **Contribute** - Follow the contribution guidelines in `CONTRIBUTING.md`

---

## Development Workflow

### Typical Development Cycle

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/add-caching
   ```

2. **Make Changes**
   - Modify code in `src/`
   - Add tests in `tests/`

3. **Run Tests**
   ```bash
   pytest --cov=src
   ```

4. **Start Server and Test Manually**
   ```bash
   uvicorn src.api.main:app --reload
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add caching for frequently asked questions"
   git push origin feature/add-caching
   ```

6. **Create Pull Request**
   - Use GitHub/GitLab UI to create PR
   - Ensure CI/CD tests pass

### Code Style

- **Format**: Use `black` for code formatting
- **Linting**: Use `ruff` for linting
- **Type Checking**: Use `mypy` for static type checking

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

---

## Docker Deployment (Optional)

### Build Docker Image

```bash
docker build -t rag-chatbot-backend:latest .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env rag-chatbot-backend:latest
```

---

## Support

- **Documentation**: `specs/001-rag-chatbot-pipeline/`
- **Issues**: https://github.com/your-org/ai-textbook/issues
- **Discussions**: https://github.com/your-org/ai-textbook/discussions

**Happy Coding!** 🚀