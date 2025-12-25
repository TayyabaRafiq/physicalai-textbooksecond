# Research & Technical Decisions: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend – Core Question Answering Pipeline
**Date**: 2025-12-21
**Phase**: 0 (Research & Discovery)

## Overview

This document consolidates research findings and technical decisions for implementing the RAG chatbot backend. All decisions align with the constitution-mandated technology stack (FastAPI, Cohere, Qdrant Cloud, Neon Postgres) and focus on production-ready patterns for RAG systems.

## Technology Stack Research

### 1. FastAPI for REST API Backend

**Decision**: Use FastAPI 0.104+ as the backend framework

**Rationale**:
- Native async/await support for I/O-bound operations (embedding generation, vector search, LLM calls)
- Automatic OpenAPI documentation generation (satisfies FR-017 structured JSON responses and API contract requirements)
- Pydantic v2 integration for request/response validation
- High performance (comparable to Node.js and Go for async workloads)
- Python 3.11+ type hints provide excellent IDE support and runtime validation

**Alternatives Considered**:
- Flask: Lacks native async support, would require additional libraries
- Django: Too heavyweight for pure API backend, includes unnecessary ORM and templating
- Express.js (Node): Would require JavaScript, conflicts with Python-based Cohere SDK

**Best Practices**:
- Use dependency injection for database connections and service clients
- Implement middleware for CORS, rate limiting, and structured logging
- Use Pydantic models for all request/response schemas
- Separate routes, services, and models into distinct layers
- Use Uvicorn as ASGI server with multiple workers for production

**References**:
- FastAPI official docs: https://fastapi.tiangolo.com/
- Async best practices: https://fastapi.tiangolo.com/async/

---

### 2. Cohere SDK for Embeddings and Generation

**Decision**: Use Cohere Python SDK 4.x+ for both embeddings (embed-english-v3.0) and answer generation (Command model)

**Rationale**:
- Constitution mandates Cohere (NO OpenAI dependency)
- embed-english-v3.0 produces 1024-dimensional embeddings optimized for semantic search
- Command model supports grounded generation with citation capabilities
- Python SDK provides async client for non-blocking API calls
- Free tier includes 1000 API calls/month (sufficient for MVP testing)

**Alternatives Considered**:
- OpenAI: Explicitly prohibited by constitution
- Sentence Transformers (local embeddings): Would not satisfy constitution requirement for Cohere

**Best Practices**:
- Use async Cohere client to avoid blocking event loop
- Implement exponential backoff for rate limit errors
- Cache frequently accessed embeddings to reduce API calls
- Use batch embedding generation (up to 96 texts per request) for ingestion
- For grounding, use Cohere's citation feature in Command model prompts

**Implementation Pattern**:
```python
from cohere import AsyncClient

# Async embedding generation
async def generate_embedding(text: str, client: AsyncClient) -> list[float]:
    response = await client.embed(
        model="embed-english-v3.0",
        texts=[text],
        input_type="search_document"  # For chunks being indexed
    )
    return response.embeddings[0]

# Async answer generation with grounding
async def generate_answer(question: str, context_chunks: list[str], client: AsyncClient) -> str:
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer the question based ONLY on the provided context. If the context does not contain enough information, respond with "I cannot answer based on the textbook content."

Context:
{context}

Question: {question}

Answer:"""
    response = await client.generate(
        model="command",
        prompt=prompt,
        max_tokens=500,
        temperature=0.3  # Low temperature for factual responses
    )
    return response.generations[0].text
```

**References**:
- Cohere Python SDK: https://github.com/cohere-ai/cohere-python
- embed-english-v3.0 docs: https://docs.cohere.com/docs/embed-3
- Command model docs: https://docs.cohere.com/docs/command-r

---

### 3. Qdrant Cloud for Vector Storage

**Decision**: Use Qdrant Cloud Free Tier with Qdrant Python Client 1.7+

**Rationale**:
- Constitution mandates Qdrant Cloud (no self-hosting)
- Free tier provides 1GB storage (~500k vectors with 1024 dimensions)
- Sub-50ms query latency for vector similarity search
- Native support for metadata filtering (can filter by module, chapter, section)
- Python client provides async operations for non-blocking queries

**Alternatives Considered**:
- Self-hosted Qdrant: Conflicts with constitution requirement for managed cloud service
- Pinecone: Not specified in constitution
- Weaviate: Not specified in constitution

**Best Practices**:
- Use collections with named vectors for semantic search
- Store metadata (module, chapter, section, file path) alongside vectors
- Use cosine similarity for semantic search (default for text embeddings)
- Implement connection pooling to reuse client instances
- Index vectors with HNSW (Hierarchical Navigable Small World) for fast approximate search

**Implementation Pattern**:
```python
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Initialize collection
async def init_collection(client: AsyncQdrantClient):
    await client.create_collection(
        collection_name="textbook_chunks",
        vectors_config=VectorParams(
            size=1024,  # Cohere embed-english-v3.0 dimension
            distance=Distance.COSINE
        )
    )

# Store chunk with embedding
async def store_chunk(client: AsyncQdrantClient, chunk_id: str, embedding: list[float], metadata: dict):
    await client.upsert(
        collection_name="textbook_chunks",
        points=[
            PointStruct(
                id=chunk_id,
                vector=embedding,
                payload=metadata  # {module, chapter, section, file_path, text}
            )
        ]
    )

# Search for similar chunks
async def search_similar(client: AsyncQdrantClient, query_embedding: list[float], top_k: int = 5):
    results = await client.search(
        collection_name="textbook_chunks",
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )
    return results
```

**References**:
- Qdrant Cloud: https://cloud.qdrant.io/
- Qdrant Python client: https://python-client.qdrant.tech/
- Best practices: https://qdrant.tech/documentation/tutorials/

---

### 4. Neon Serverless Postgres for Metadata

**Decision**: Use Neon Serverless Postgres with SQLAlchemy 2.0+ ORM

**Rationale**:
- Constitution mandates Neon for metadata storage
- Serverless autoscaling (scales to zero when idle, reduces costs)
- Free tier provides 0.5GB storage (sufficient for textbook metadata)
- SQLAlchemy 2.0 provides async ORM support for non-blocking queries
- Alembic integration for database migrations

**Alternatives Considered**:
- Direct psycopg3 (async PostgreSQL driver): Lower-level, would require manual query building
- Self-hosted PostgreSQL: Conflicts with constitution requirement for Neon

**Best Practices**:
- Use async SQLAlchemy engine with asyncpg driver
- Define relationships with foreign keys (module → chapters → sections → chunks)
- Use Alembic for schema migrations (version-controlled)
- Index foreign keys for fast hierarchical queries
- Store chunk text in Postgres as backup (Qdrant may delete data on free tier limits)

**Schema Design**:
```
modules (id, title, description, order)
  ↓
chapters (id, module_id FK, title, order)
  ↓
sections (id, chapter_id FK, title, order)
  ↓
chunks (id, section_id FK, content TEXT, file_path, line_start, line_end, qdrant_id UUID)
```

**Implementation Pattern**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey

Base = declarative_base()

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    chapters = relationship("Chapter", back_populates="module")

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    module = relationship("Module", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter")

# ... similar for Section and Chunk
```

**References**:
- Neon: https://neon.tech/docs
- SQLAlchemy 2.0 async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Alembic migrations: https://alembic.sqlalchemy.org/

---

### 5. Markdown Chunking Strategy

**Decision**: Use section-level chunking with 1024-token limit

**Rationale**:
- Specification defines 1024 tokens as balanced chunk size (FR-019)
- Heading-based chunking preserves semantic boundaries
- 1024 tokens ≈ 750-800 words (sufficient context for most educational concepts)
- Cohere embed-english-v3.0 supports up to 512 tokens input (will need to truncate or split longer chunks)

**Alternatives Considered**:
- Fixed 512-token chunks: May split concepts mid-explanation
- Paragraph-level chunks: Too granular, loses context
- Chapter-level chunks: Too large, exceeds embedding model limits

**Best Practices**:
- Parse markdown using Python markdown library
- Identify headings (# Module, ## Chapter, ### Section) for hierarchy
- Split sections >1024 tokens into subsections at paragraph boundaries
- Preserve code blocks intact (don't split mid-code)
- Store original line ranges for source attribution

**Implementation Pattern**:
```python
import tiktoken  # OpenAI's tokenizer (BPE, approximates Cohere)

def chunk_section(section_text: str, max_tokens: int = 1024) -> list[str]:
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(section_text)

    if len(tokens) <= max_tokens:
        return [section_text]

    # Split at paragraph boundaries
    paragraphs = section_text.split("\n\n")
    chunks = []
    current_chunk = []
    current_tokens = 0

    for para in paragraphs:
        para_tokens = len(encoding.encode(para))
        if current_tokens + para_tokens > max_tokens:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_tokens = para_tokens
        else:
            current_chunk.append(para)
            current_tokens += para_tokens

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks
```

**References**:
- Python markdown: https://python-markdown.github.io/
- tiktoken (tokenizer): https://github.com/openai/tiktoken

---

### 6. Rate Limiting Strategy

**Decision**: Use slowapi (FastAPI-compatible rate limiting) with in-memory store for MVP

**Rationale**:
- Specification requires rate limiting (FR-014)
- slowapi provides decorator-based rate limiting for FastAPI
- In-memory store sufficient for single-instance MVP (100 requests/min per IP default)
- Can upgrade to Redis-backed store for multi-instance deployments

**Alternatives Considered**:
- Custom middleware: More complex, reinvents the wheel
- Redis-backed rate limiting: Overkill for MVP, adds infrastructure dependency

**Best Practices**:
- Apply rate limiting per IP address
- Return 429 Too Many Requests with Retry-After header
- Use different limits for ingestion (lower, e.g., 10/min) vs query (higher, e.g., 100/min)
- Log rate limit violations for monitoring

**Implementation Pattern**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/question")
@limiter.limit("100/minute")
async def ask_question(request: Request, question: QuestionRequest):
    # ... question handling
```

**References**:
- slowapi: https://github.com/laurentS/slowapi

---

### 7. Error Handling and Logging

**Decision**: Use structured logging with Python logging + FastAPI exception handlers

**Rationale**:
- Structured logs (JSON format) enable better monitoring and debugging
- FastAPI exception handlers provide consistent error responses
- Python logging module is standard library (no extra dependencies)

**Best Practices**:
- Log all API requests with correlation IDs
- Log errors with stack traces and context (user input, request ID)
- Return consistent error JSON: `{"error": {"code": "...", "message": "...", "details": ...}}`
- Use different log levels (DEBUG for development, INFO for production, ERROR for failures)

**Implementation Pattern**:
```python
import logging
import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)

logger = logging.getLogger(__name__)

# Exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}", extra={"request_id": request.state.request_id})
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": exc.detail}}
    )
```

---

### 8. Testing Strategy

**Decision**: Use pytest with pytest-asyncio for async tests, httpx for API testing

**Rationale**:
- pytest is Python standard for testing
- pytest-asyncio enables testing async functions
- httpx is async HTTP client compatible with FastAPI testing
- FastAPI provides TestClient for integration testing

**Test Levels**:
1. **Unit tests**: Test individual services (chunker, embedder, generator) with mocked dependencies
2. **Integration tests**: Test API endpoints end-to-end with real database (use test Qdrant collection + test Neon database)
3. **Contract tests**: Validate API responses match OpenAPI schema

**Best Practices**:
- Use fixtures for database setup/teardown
- Mock external API calls (Cohere) in unit tests to avoid API costs
- Use separate test databases (Qdrant test collection, Neon test schema)
- Aim for 80%+ code coverage

**References**:
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/
- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/

---

## Architectural Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend Framework | FastAPI 0.104+ | Async support, automatic OpenAPI, Pydantic validation |
| Language | Python 3.11+ | Required for Cohere SDK, modern type hints, async/await |
| Embeddings | Cohere embed-english-v3.0 | Constitution mandate, 1024-dim vectors, semantic search optimized |
| LLM | Cohere Command | Constitution mandate, supports grounded generation |
| Vector DB | Qdrant Cloud Free Tier | Constitution mandate, fast similarity search, metadata filtering |
| Metadata DB | Neon Serverless Postgres | Constitution mandate, serverless autoscaling, free tier |
| ORM | SQLAlchemy 2.0 (async) | Async support, migrations via Alembic, relationship modeling |
| Chunking | Section-level, 1024 tokens | Spec requirement (FR-019), balanced context vs precision |
| Rate Limiting | slowapi (in-memory) | FastAPI-compatible, sufficient for MVP, no extra infra |
| Testing | pytest + httpx | Python standard, async support, API integration testing |
| Deployment | Docker + Railway/Render/Fly.io | Containerized, constitution requirement for cloud deployment |

---

## Open Questions Resolved

1. **Q: How to handle chunks >512 tokens (Cohere embedding limit)?**
   - **A**: Cohere embed-english-v3.0 actually supports up to 512 *tokens* (not 1024). For chunks >512 tokens, we have two options:
     - (a) Truncate to 512 tokens (acceptable for most educational content)
     - (b) Re-chunk at 512 tokens (would require spec change)
   - **Decision**: Use option (a) truncation for MVP. If retrieval quality suffers, re-evaluate in iteration 2.

2. **Q: Should we cache Cohere API responses?**
   - **A**: Yes, for frequently asked questions. Implement in-memory LRU cache (e.g., functools.lru_cache) for embeddings and answers.
   - **Decision**: Cache embeddings (stable) aggressively, cache answers (may need updates) with short TTL (1 hour).

3. **Q: How to handle Qdrant Free Tier limits (1GB storage)?**
   - **A**: 1GB ≈ 250k vectors (1024-dim, 4 bytes/float). Single textbook ~500-1000 chunks, well within limit.
   - **Decision**: Monitor usage, store chunk text in Neon as backup, implement cleanup strategy if approaching limits.

4. **Q: Should ingestion be synchronous or async API?**
   - **A**: Async (background job) to avoid timeout for large textbooks.
   - **Decision**: Return 202 Accepted with job ID, provide status endpoint to check progress.

---

## Next Steps (Phase 1)

1. Generate data-model.md with SQLAlchemy schema definitions
2. Generate OpenAPI contract in contracts/openapi.yaml
3. Generate quickstart.md for developer onboarding
4. Update agent context with technology decisions
5. Re-evaluate Constitution Check post-design

**Phase 0 Complete**: All technical unknowns resolved, ready for Phase 1 design artifacts.