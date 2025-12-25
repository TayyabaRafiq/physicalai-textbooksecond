# Data Model: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend – Core Question Answering Pipeline
**Date**: 2025-12-21
**Phase**: 1 (Design & Contracts)

## Overview

This document defines the data models for the RAG chatbot backend, including both relational metadata (Neon Postgres) and vector storage (Qdrant Cloud). All models support the hierarchical structure of textbook content (module → chapter → section → chunk) and enable source attribution for generated answers.

---

## Neon Postgres Schema (Metadata)

### Entity-Relationship Diagram

```
┌─────────────────┐
│    Module       │
│─────────────────│
│ id (PK)         │
│ title           │
│ description     │
│ order           │
│ created_at      │
│ updated_at      │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│    Chapter      │
│─────────────────│
│ id (PK)         │
│ module_id (FK)  │
│ title           │
│ order           │
│ created_at      │
│ updated_at      │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│    Section      │
│─────────────────│
│ id (PK)         │
│ chapter_id (FK) │
│ title           │
│ order           │
│ created_at      │
│ updated_at      │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────────────┐
│         Chunk           │
│─────────────────────────│
│ id (PK)                 │
│ section_id (FK)         │
│ content (TEXT)          │
│ token_count             │
│ file_path               │
│ line_start              │
│ line_end                │
│ qdrant_id (UUID)        │
│ created_at              │
│ updated_at              │
└─────────────────────────┘

┌─────────────────────────┐
│    QuestionLog          │
│─────────────────────────│
│ id (PK)                 │
│ question_text           │
│ mode (enum)             │
│ selected_text (TEXT)    │
│ user_ip                 │
│ created_at              │
└─────────────────────────┘
        │
        │ 1:1
        ▼
┌─────────────────────────┐
│      AnswerLog          │
│─────────────────────────│
│ id (PK)                 │
│ question_id (FK)        │
│ answer_text             │
│ sources (JSONB)         │
│ retrieved_chunk_ids     │
│ model_used              │
│ response_time_ms        │
│ created_at              │
└─────────────────────────┘
```

---

### Table Definitions

#### 1. Module

Represents a top-level module in the textbook (e.g., "Module 1: Introduction to Physical AI").

```sql
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_modules_order ON modules("order");
```

**Constraints**:
- `title` must be unique within the textbook
- `order` determines display sequence (1, 2, 3, ...)

---

#### 2. Chapter

Represents a chapter within a module (e.g., "Chapter 1: What is Physical AI?").

```sql
CREATE TABLE chapters (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chapters_module_id ON chapters(module_id);
CREATE INDEX idx_chapters_order ON chapters("order");
```

**Constraints**:
- `module_id` foreign key ensures chapter belongs to a valid module
- `order` is scoped within the parent module (chapter 1, 2, 3 per module)

---

#### 3. Section

Represents a section within a chapter (e.g., "Section 1.1: Defining Physical AI").

```sql
CREATE TABLE sections (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sections_chapter_id ON sections(chapter_id);
CREATE INDEX idx_sections_order ON sections("order");
```

**Constraints**:
- `chapter_id` foreign key ensures section belongs to a valid chapter
- `order` is scoped within the parent chapter (section 1, 2, 3 per chapter)

---

#### 4. Chunk

Represents a semantically meaningful piece of content for RAG retrieval (max 1024 tokens).

```sql
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    line_start INTEGER NOT NULL,
    line_end INTEGER NOT NULL,
    qdrant_id UUID NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chunks_section_id ON chunks(section_id);
CREATE INDEX idx_chunks_qdrant_id ON chunks(qdrant_id);
CREATE INDEX idx_chunks_file_path ON chunks(file_path);
```

**Constraints**:
- `section_id` foreign key ensures chunk belongs to a valid section
- `content` stores the full text of the chunk (backup for Qdrant vector)
- `token_count` tracks chunk size (should be ≤1024)
- `file_path` + `line_start`/`line_end` enable source attribution
- `qdrant_id` links to the corresponding vector in Qdrant Cloud (must be unique)

---

#### 5. QuestionLog

Records all user questions for monitoring and analytics (satisfies FR-018).

```sql
CREATE TYPE question_mode AS ENUM ('full_textbook', 'selected_text');

CREATE TABLE question_log (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    mode question_mode NOT NULL,
    selected_text TEXT,  -- Only populated for selected_text mode
    user_ip VARCHAR(45),  -- IPv4 or IPv6 (for rate limiting)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_question_log_created_at ON question_log(created_at);
CREATE INDEX idx_question_log_user_ip ON question_log(user_ip);
```

**Constraints**:
- `mode` determines question answering strategy (full_textbook or selected_text)
- `selected_text` is NULL for full_textbook mode
- `user_ip` enables rate limiting per IP address

---

#### 6. AnswerLog

Records generated answers with source citations and performance metrics.

```sql
CREATE TABLE answer_log (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES question_log(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    sources JSONB NOT NULL,  -- Array of {module, chapter, section, chunk_id}
    retrieved_chunk_ids INTEGER[] NOT NULL,  -- Array of chunk IDs from Qdrant search
    model_used VARCHAR(50) NOT NULL,  -- e.g., "command-r-plus"
    response_time_ms INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_answer_log_question_id ON answer_log(question_id);
CREATE INDEX idx_answer_log_created_at ON answer_log(created_at);
```

**Constraints**:
- `question_id` foreign key links answer to its question (1:1 relationship)
- `sources` stores structured source citations as JSONB for querying
- `retrieved_chunk_ids` tracks which chunks were used for generation
- `response_time_ms` enables performance monitoring

**Example `sources` JSONB**:
```json
[
  {
    "module": "Module 1: Introduction to Physical AI",
    "chapter": "Chapter 1: What is Physical AI?",
    "section": "Section 1.1: Defining Physical AI",
    "chunk_id": 42
  },
  {
    "module": "Module 1: Introduction to Physical AI",
    "chapter": "Chapter 2: Key Concepts",
    "section": "Section 2.1: Embodied AI",
    "chunk_id": 58
  }
]
```

---

## Qdrant Cloud Schema (Vector Storage)

### Collection: `textbook_chunks`

**Configuration**:
```python
{
    "name": "textbook_chunks",
    "vectors": {
        "size": 1024,  # Cohere embed-english-v3.0 dimension
        "distance": "Cosine"  # Cosine similarity for semantic search
    },
    "hnsw_config": {
        "m": 16,  # Number of edges per node (default: 16)
        "ef_construct": 100  # Size of candidate list (default: 100)
    }
}
```

**Point Structure**:
Each point in Qdrant represents one chunk with its embedding and metadata.

```python
{
    "id": "uuid-string",  # UUID matching chunks.qdrant_id in Postgres
    "vector": [0.1, -0.2, 0.3, ...],  # 1024-dimensional embedding
    "payload": {
        "chunk_id": 42,  # Postgres chunks.id
        "section_id": 10,  # Postgres sections.id
        "chapter_id": 3,  # Postgres chapters.id
        "module_id": 1,  # Postgres modules.id
        "module_title": "Module 1: Introduction to Physical AI",
        "chapter_title": "Chapter 1: What is Physical AI?",
        "section_title": "Section 1.1: Defining Physical AI",
        "file_path": "content/module1/chapter1.md",
        "line_start": 10,
        "line_end": 25,
        "content": "Full text of the chunk (for retrieval display)...",
        "token_count": 512
    }
}
```

**Indexing Strategy**:
- HNSW (Hierarchical Navigable Small World) for approximate nearest neighbor search
- Cosine distance for semantic similarity
- Metadata payload enables filtering (e.g., search only within Module 1)

**Query Example**:
```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Search with module filter
results = await client.search(
    collection_name="textbook_chunks",
    query_vector=query_embedding,
    limit=5,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="module_id",
                match=MatchValue(value=1)  # Only search Module 1
            )
        ]
    )
)
```

---

## Pydantic Models (Request/Response Schemas)

### Request Models

#### 1. IngestionRequest

```python
from pydantic import BaseModel, Field

class IngestionRequest(BaseModel):
    file_path: str = Field(..., description="Path to markdown file to ingest")
    module_title: str = Field(..., description="Title of the module")
    module_description: str | None = Field(None, description="Optional module description")
    module_order: int = Field(..., description="Order of the module in the textbook", ge=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file_path": "content/module1.md",
                    "module_title": "Module 1: Introduction to Physical AI",
                    "module_description": "Foundational concepts in Physical AI",
                    "module_order": 1
                }
            ]
        }
    }
```

#### 2. QuestionRequest (Full Textbook Mode)

```python
class QuestionRequest(BaseModel):
    question: str = Field(..., description="User's question", min_length=5, max_length=500)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"question": "What is physical AI?"}
            ]
        }
    }
```

#### 3. SelectedTextQuestionRequest

```python
class SelectedTextQuestionRequest(BaseModel):
    question: str = Field(..., description="User's question about selected text", min_length=5, max_length=500)
    selected_text: str = Field(..., description="Text selected by user", min_length=10, max_length=5000)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Can you explain this concept?",
                    "selected_text": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents like robots..."
                }
            ]
        }
    }
```

### Response Models

#### 1. IngestionResponse

```python
class IngestionResponse(BaseModel):
    job_id: str = Field(..., description="ID to track ingestion job status")
    status: str = Field(..., description="Job status: accepted, processing, completed, failed")
    message: str = Field(..., description="Human-readable status message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "job_id": "ing-123e4567-e89b-12d3-a456-426614174000",
                    "status": "accepted",
                    "message": "Ingestion job accepted. Check /api/v1/ingestion/status/{job_id} for progress."
                }
            ]
        }
    }
```

#### 2. AnswerResponse

```python
from typing import List

class SourceCitation(BaseModel):
    module: str
    chapter: str
    section: str
    chunk_id: int

class AnswerResponse(BaseModel):
    answer: str = Field(..., description="Generated answer to the question")
    sources: List[SourceCitation] = Field(..., description="Source citations for the answer")
    mode: str = Field(..., description="Question mode: full_textbook or selected_text")
    confidence: str = Field(..., description="Confidence level: high, medium, low")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents, such as robots. These systems combine perception, reasoning, and action to operate in real-world environments.",
                    "sources": [
                        {
                            "module": "Module 1: Introduction to Physical AI",
                            "chapter": "Chapter 1: What is Physical AI?",
                            "section": "Section 1.1: Defining Physical AI",
                            "chunk_id": 42
                        }
                    ],
                    "mode": "full_textbook",
                    "confidence": "high"
                }
            ]
        }
    }
```

#### 3. ErrorResponse

```python
class ErrorDetail(BaseModel):
    code: str = Field(..., description="Error code (e.g., INVALID_INPUT, NOT_FOUND)")
    message: str = Field(..., description="Human-readable error message")
    details: dict | None = Field(None, description="Additional error context")

class ErrorResponse(BaseModel):
    error: ErrorDetail

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": {
                        "code": "NO_RELEVANT_CONTENT",
                        "message": "I cannot answer based on the textbook content",
                        "details": {"question": "What is the meaning of life?"}
                    }
                }
            ]
        }
    }
```

---

## Data Validation Rules

### Module
- `title`: Required, 1-255 characters, unique
- `order`: Required, positive integer, unique

### Chapter
- `title`: Required, 1-255 characters
- `order`: Required, positive integer, unique within module

### Section
- `title`: Required, 1-255 characters
- `order`: Required, positive integer, unique within chapter

### Chunk
- `content`: Required, non-empty text
- `token_count`: Required, 1-1024 (enforced by chunking logic)
- `file_path`: Required, valid file path
- `line_start`, `line_end`: Required, positive integers, line_start ≤ line_end
- `qdrant_id`: Required, valid UUID, unique

### QuestionRequest
- `question`: Required, 5-500 characters

### SelectedTextQuestionRequest
- `question`: Required, 5-500 characters
- `selected_text`: Required, 10-5000 characters

---

## State Transitions

### Ingestion Job States

```
[Accepted] → [Processing] → [Completed]
                    ↓
                [Failed]
```

- **Accepted**: Job queued, not yet started
- **Processing**: Currently ingesting content (parsing, chunking, embedding, storing)
- **Completed**: All chunks successfully stored in Qdrant and Neon
- **Failed**: Error during ingestion (parsing failure, API error, database error)

---

## Database Migrations (Alembic)

**Migration Strategy**:
- Use Alembic for version-controlled schema changes
- Each migration has `upgrade()` and `downgrade()` functions
- Migrations are numbered sequentially (e.g., 001_initial_schema.py)

**Initial Migration** (001_initial_schema.py):
```python
def upgrade():
    op.create_table('modules', ...)
    op.create_table('chapters', ...)
    op.create_table('sections', ...)
    op.create_table('chunks', ...)
    op.create_table('question_log', ...)
    op.create_table('answer_log', ...)

def downgrade():
    op.drop_table('answer_log')
    op.drop_table('question_log')
    op.drop_table('chunks')
    op.drop_table('sections')
    op.drop_table('chapters')
    op.drop_table('modules')
```

---

## Summary

- **Neon Postgres**: Stores hierarchical metadata (modules → chapters → sections → chunks) and query logs
- **Qdrant Cloud**: Stores vector embeddings with payload metadata for semantic search
- **Pydantic Models**: Enforce request/response validation and auto-generate OpenAPI documentation
- **Migrations**: Alembic tracks schema changes for reproducible deployments

**Next**: Generate OpenAPI contract in contracts/openapi.yaml