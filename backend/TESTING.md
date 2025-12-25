# Testing Guide: RAG Chatbot Backend

**Version**: 0.1.0
**Date**: 2025-12-23
**Status**: Ready for Testing

## Overview

This document provides comprehensive testing instructions for the Physical AI RAG Chatbot Backend. All tests should be run after fixing database credentials in `.env`.

---

## Prerequisites

### 1. Environment Setup

Ensure `.env` file has valid credentials:
```bash
# Cohere API Configuration
COHERE_API_KEY=your-valid-cohere-api-key

# Qdrant Cloud Configuration
QDRANT_API_KEY=your-valid-qdrant-api-key
QDRANT_URL=your-qdrant-cluster-url

# Neon Serverless Postgres Configuration
NEON_DATABASE_URL=postgresql+asyncpg://user:password@host/database?ssl=require

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 2. Run Database Migration

```bash
uv run alembic upgrade head
```

Expected output: Tables created successfully (modules, chapters, sections, chunks, question_log, answer_log)

### 3. Start the Server

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Test Suite

### Phase 1: Health Check

#### Test 1.1: Basic Health Check

**Endpoint**: `GET /health`

```bash
curl http://localhost:8000/health
```

**Expected Response (200 OK)**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "services": {
    "database": {
      "available": true,
      "message": "Database connection successful",
      "latency_ms": 50
    },
    "qdrant": {
      "available": true,
      "message": "Qdrant available (1 collections)",
      "latency_ms": 100
    },
    "cohere": {
      "available": true,
      "message": "Cohere API available",
      "latency_ms": 200
    }
  }
}
```

**Pass Criteria**:
- Status code: 200
- `status`: "healthy" (if all services up) or "degraded" (if some down)
- All services have `available` field
- Response time < 5 seconds

---

### Phase 2: Content Ingestion

#### Test 2.1: Prepare Test Content

Create a sample markdown file `test_module.md`:

```markdown
## Chapter 1: Introduction to Physical AI

### Section 1.1: Defining Physical AI

Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents, such as robots. These systems combine perception, reasoning, and action to operate in real-world environments.

Key characteristics of Physical AI:
- Embodiment: Physical form or presence
- Perception: Sensing the environment
- Action: Manipulating the physical world
- Learning: Adapting from experience

### Section 1.2: Applications

Physical AI has applications in:
- Manufacturing and industrial automation
- Healthcare and surgery
- Autonomous vehicles
- Space exploration
```

#### Test 2.2: Submit Ingestion Request

**Endpoint**: `POST /api/v1/ingestion`

```bash
curl -X POST http://localhost:8000/api/v1/ingestion \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "test_module.md",
    "module_title": "Module 1: Introduction to Physical AI",
    "module_description": "Foundational concepts in Physical AI",
    "module_order": 1
  }'
```

**Expected Response (202 Accepted)**:
```json
{
  "job_id": "ing-123e4567-e89b-12d3-a456-426614174000",
  "status": "accepted",
  "message": "Ingestion job accepted. Check /api/v1/ingestion/status/{job_id} for progress."
}
```

**Pass Criteria**:
- Status code: 202
- `job_id` returned (UUID format)
- `status`: "accepted"

#### Test 2.3: Check Ingestion Status

**Endpoint**: `GET /api/v1/ingestion/status/{job_id}`

```bash
curl http://localhost:8000/api/v1/ingestion/status/ing-123e4567-e89b-12d3-a456-426614174000
```

**Expected Response (200 OK)**:
```json
{
  "job_id": "ing-123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "message": "Successfully ingested 4 chunks",
  "chunks_processed": 4,
  "error": null
}
```

**Pass Criteria**:
- Status code: 200
- `status`: "completed" (or "processing" if still running)
- `chunks_processed` > 0
- No error message

#### Test 2.4: Validate Database Storage

```bash
# Check that chunks exist in database
uv run python -c "
import asyncio
from sqlalchemy import select, func
from app.models.database import get_session_factory, Module, Chapter, Section, Chunk

async def check():
    session_factory = get_session_factory()
    async with session_factory() as session:
        # Count modules
        result = await session.execute(select(func.count(Module.id)))
        print(f'Modules: {result.scalar()}')

        # Count chunks
        result = await session.execute(select(func.count(Chunk.id)))
        print(f'Chunks: {result.scalar()}')

asyncio.run(check())
"
```

**Expected Output**:
```
Modules: 1
Chunks: 4 (or more, depending on content)
```

**Pass Criteria**:
- At least 1 module created
- At least 2 chunks created
- No errors

---

### Phase 3: Question Answering (Full Textbook)

#### Test 3.1: Ask Simple Question

**Endpoint**: `POST /api/v1/question`

```bash
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is physical AI?"
  }'
```

**Expected Response (200 OK)**:
```json
{
  "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents, such as robots. These systems combine perception, reasoning, and action to operate in real-world environments.",
  "sources": [
    {
      "module": "Module 1: Introduction to Physical AI",
      "chapter": "Chapter 1: Introduction to Physical AI",
      "section": "Section 1.1: Defining Physical AI",
      "chunk_id": 1
    }
  ],
  "mode": "full_textbook",
  "confidence": "high"
}
```

**Pass Criteria**:
- Status code: 200
- `answer` contains relevant information
- `sources` array not empty
- `confidence`: "high", "medium", or "low"
- `mode`: "full_textbook"
- Response time < 5 seconds (check `X-Process-Time` header)

#### Test 3.2: Ask Complex Question

```bash
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key characteristics of Physical AI systems?"
  }'
```

**Pass Criteria**:
- Answer mentions multiple characteristics
- Multiple sources cited if applicable
- Answer is coherent and beginner-friendly

#### Test 3.3: Ask Irrelevant Question

```bash
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the meaning of life?"
  }'
```

**Expected Response**:
```json
{
  "answer": "I cannot answer based on the textbook content. No relevant information was found.",
  "sources": [],
  "mode": "full_textbook",
  "confidence": "low"
}
```

**Pass Criteria**:
- Answer indicates no relevant content found
- Sources array empty or minimal
- Confidence: "low"

---

### Phase 4: Question Answering (Selected Text)

#### Test 4.1: Ask About Selected Text

**Endpoint**: `POST /api/v1/question/selected-text`

```bash
curl -X POST http://localhost:8000/api/v1/question/selected-text \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does embodiment mean in this context?",
    "selected_text": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents, such as robots. Embodiment means having a physical form or presence."
  }'
```

**Expected Response (200 OK)**:
```json
{
  "answer": "Embodiment in this context means having a physical form or presence, such as a robot that can interact with the physical world.",
  "sources": [],
  "mode": "selected_text",
  "confidence": "medium"
}
```

**Pass Criteria**:
- Answer based strictly on selected text
- `sources`: empty (no Qdrant retrieval)
- `mode`: "selected_text"
- Answer does not use external knowledge

#### Test 4.2: Insufficient Selected Text

```bash
curl -X POST http://localhost:8000/api/v1/question/selected-text \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How does machine learning work?",
    "selected_text": "Physical AI systems use perception."
  }'
```

**Expected Response**:
```json
{
  "answer": "I cannot answer based on the selected text alone.",
  "sources": [],
  "mode": "selected_text",
  "confidence": "medium"
}
```

**Pass Criteria**:
- Answer indicates insufficient information
- No hallucination or external knowledge used

---

### Phase 5: Edge Cases & Error Handling

#### Test 5.1: Invalid Request (Missing Required Field)

```bash
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response (400 Bad Request)**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "errors": [
        {
          "field": "body -> question",
          "message": "field required",
          "type": "value_error.missing"
        }
      ]
    }
  }
}
```

**Pass Criteria**:
- Status code: 400
- Error code: "VALIDATION_ERROR"
- Clear error message

#### Test 5.2: Question Too Short

```bash
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "AI?"
  }'
```

**Expected Response (400 Bad Request)**:
- Validation error indicating minimum length not met

#### Test 5.3: Question Too Long

```bash
# Generate 600 character question
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"$(python -c 'print(\"What is AI? \" * 100)')\"}"
```

**Expected Response (400 Bad Request)**:
- Validation error indicating maximum length exceeded

#### Test 5.4: Special Characters in Question

```bash
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is <script>alert(\"XSS\")</script> in Physical AI?"
  }'
```

**Pass Criteria**:
- Question processed safely (no code injection)
- Answer returned normally
- Special characters sanitized

---

### Phase 6: Performance & Monitoring

#### Test 6.1: Response Time Monitoring

Check `X-Process-Time` header in all responses:

```bash
curl -i http://localhost:8000/health
```

**Pass Criteria**:
- Header `X-Process-Time` present (value in milliseconds)
- Health check < 5000ms
- Question answering < 5000ms
- Ingestion < 60000ms

#### Test 6.2: Concurrent Requests

```bash
# Run 10 concurrent question requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/v1/question \
    -H "Content-Type: application/json" \
    -d '{"question": "What is physical AI?"}' &
done
wait
```

**Pass Criteria**:
- All requests complete successfully
- No 500 errors
- Response times reasonable (<10s)

#### Test 6.3: Check Logs

```bash
# Logs should show structured JSON format
tail -f logs/app.log  # If logging to file
```

**Pass Criteria**:
- Logs in JSON format
- Request/response times logged
- Error messages include stack traces

---

### Phase 7: API Documentation

#### Test 7.1: OpenAPI Documentation

Visit: `http://localhost:8000/docs`

**Pass Criteria**:
- Swagger UI loads successfully
- All endpoints visible (health, ingestion, question)
- Request/response schemas documented
- Try it out feature works

#### Test 7.2: ReDoc Documentation

Visit: `http://localhost:8000/redoc`

**Pass Criteria**:
- ReDoc UI loads successfully
- All endpoints documented
- Examples provided

#### Test 7.3: OpenAPI JSON

```bash
curl http://localhost:8000/openapi.json | jq .
```

**Pass Criteria**:
- Valid OpenAPI 3.0 JSON
- All endpoints present
- Schemas match implementation

---

## Manual Test Checklist

### Pre-Flight Checks
- [ ] `.env` file has valid credentials
- [ ] Database migration completed successfully
- [ ] Server starts without errors
- [ ] Health check returns "healthy" status

### Content Ingestion
- [ ] Can ingest markdown file successfully
- [ ] Job status endpoint tracks progress
- [ ] Chunks stored in Postgres
- [ ] Vectors stored in Qdrant
- [ ] Hierarchical structure preserved (module → chapter → section → chunk)

### Question Answering (Full Textbook)
- [ ] Simple questions answered correctly
- [ ] Answers grounded in textbook content
- [ ] Source citations included
- [ ] Confidence levels appropriate
- [ ] Irrelevant questions handled gracefully

### Question Answering (Selected Text)
- [ ] Answers based only on selected text
- [ ] No external knowledge used
- [ ] Insufficient text handled gracefully

### Error Handling
- [ ] Validation errors return 400 with clear messages
- [ ] Missing fields caught
- [ ] Length constraints enforced
- [ ] Special characters handled safely

### Performance
- [ ] Response times within acceptable limits
- [ ] `X-Process-Time` header present
- [ ] Concurrent requests handled
- [ ] No memory leaks during load

### Documentation
- [ ] OpenAPI docs accessible
- [ ] All endpoints documented
- [ ] Examples provided
- [ ] Schemas match implementation

---

## Automated Testing (Future)

### Unit Tests
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### Contract Tests
```bash
pytest tests/contract/ -v
```

---

## Troubleshooting

### Issue: Database Connection Failed

**Symptoms**: Health check shows database unavailable

**Solutions**:
1. Verify `NEON_DATABASE_URL` in `.env`
2. Check database is accessible: `psql $NEON_DATABASE_URL`
3. Ensure migrations run: `uv run alembic current`

### Issue: Qdrant Connection Failed

**Symptoms**: Health check shows Qdrant unavailable

**Solutions**:
1. Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
2. Test connectivity: `curl -H "api-key: $QDRANT_API_KEY" $QDRANT_URL/collections`

### Issue: Cohere API Failed

**Symptoms**: Question answering fails with 500 error

**Solutions**:
1. Verify `COHERE_API_KEY` in `.env`
2. Check API quota: Visit Cohere dashboard
3. Test API: `curl -H "Authorization: Bearer $COHERE_API_KEY" https://api.cohere.ai/v1/models`

### Issue: No Chunks Generated

**Symptoms**: Ingestion completes but 0 chunks

**Solutions**:
1. Check markdown file format (must have `## Chapter` and `### Section` headings)
2. Verify file is accessible at specified path
3. Check logs for parsing errors

---

## Success Criteria

The system is considered **ready for deployment** when:

1. ✅ All health checks pass
2. ✅ Content ingestion works end-to-end
3. ✅ Question answering produces grounded answers
4. ✅ Source citations are accurate
5. ✅ Edge cases handled gracefully
6. ✅ Performance within acceptable limits (<5s for Q&A)
7. ✅ All API endpoints documented
8. ✅ No critical errors in logs

---

## Appendix: Sample Test Data

### Sample Markdown Files

Located in `tests/fixtures/`:
- `module1_intro.md` - Introduction to Physical AI
- `module2_robotics.md` - Robotics and Automation
- `module3_perception.md` - Perception Systems

### Sample Questions

Located in `tests/fixtures/questions.json`:
```json
{
  "simple": [
    "What is physical AI?",
    "What are robots?",
    "How does perception work?"
  ],
  "complex": [
    "How do Physical AI systems combine perception, reasoning, and action?",
    "What are the main challenges in deploying autonomous robots?"
  ],
  "irrelevant": [
    "What is the meaning of life?",
    "How do I cook pasta?",
    "What's the weather today?"
  ]
}
```

---

**End of Testing Guide**

For issues or questions, check:
- GitHub Issues: https://github.com/your-repo/issues
- Documentation: README.md
- Spec: specs/001-rag-chatbot-pipeline/spec.md
