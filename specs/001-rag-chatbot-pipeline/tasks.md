# Tasks: RAG Chatbot Backend – Core Question Answering Pipeline

**Feature**: RAG Chatbot Backend – Core Question Answering Pipeline
**Branch**: `001-rag-chatbot-pipeline`
**Date**: 2025-12-21
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This document breaks down the implementation into testable, executable tasks organized by user story priority. Each phase represents a complete, independently testable increment of functionality.

**User Stories** (from spec.md):
- **US1 (P1)**: Content Ingestion for RAG System - Ingest, chunk, embed, and store textbook content
- **US2 (P2)**: Full Textbook Question Answering - Answer questions using full textbook retrieval with source citations
- **US3 (P3)**: Selected Text Question Answering - Answer questions restricted to user-selected text only

**Implementation Strategy**: MVP-first, incremental delivery. Complete US1 first for foundational capability, then US2 for core value, then US3 for enhanced UX.

---

## Task Execution Guide

### Checkbox Format

Every task follows this strict format:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

- `[TaskID]`: Sequential number (T001, T002, etc.)
- `[P]`: Present ONLY if task can run in parallel with others
- `[Story]`: User story label ([US1], [US2], [US3]) - ONLY in user story phases
- Description: Clear action with exact file path

### Parallelization

Tasks marked `[P]` can be executed in parallel because they:
- Modify different files
- Have no dependencies on incomplete tasks
- Are independently testable

### Dependencies

See "User Story Dependencies" section for completion order.

---

## Phase 1: Project Setup

**Goal**: Initialize Python project with all dependencies and configuration

**Tasks**:

- [ ] T001 Create project directory structure per plan.md (backend/src/, backend/tests/, etc.)
- [ ] T002 [P] Create pyproject.toml with Python 3.11+ and all dependencies (FastAPI, Cohere, Qdrant, SQLAlchemy, pytest, etc.)
- [ ] T003 [P] Create backend/.env.example with all required environment variables (COHERE_API_KEY, QDRANT_API_KEY, QDRANT_URL, NEON_DATABASE_URL)
- [ ] T004 [P] Create backend/.gitignore to exclude .env, __pycache__, *.pyc, venv/, .pytest_cache/, htmlcov/
- [ ] T005 [P] Create backend/README.md with project overview, setup instructions, and quick start guide
- [ ] T006 Create empty __init__.py files in all Python package directories (src/, src/api/, src/models/, src/services/, src/core/, src/utils/, tests/)
- [ ] T007 [P] Create backend/Dockerfile for containerized deployment (Python 3.11+ base image, install dependencies, copy src/, expose port 8000, run uvicorn)
- [ ] T008 Install all dependencies and verify environment: `pip install -e ".[dev]"` runs without errors

**Acceptance**: Project structure matches plan.md, all dependencies install successfully, .env.example documents all required variables.

---

## Phase 2: Foundational Infrastructure

**Goal**: Set up core infrastructure (config, logging, database connections) that all user stories depend on

**Tasks**:

- [ ] T009 Create backend/src/core/config.py with Pydantic BaseSettings for environment variables (Cohere API key, Qdrant URL/API key, Neon DB URL, log level, rate limits)
- [ ] T010 [P] Create backend/src/core/logging.py with structured JSON logging configuration (log level from config, request ID middleware)
- [ ] T011 [P] Create backend/src/core/dependencies.py with FastAPI dependency injection functions (get_db_session, get_qdrant_client, get_cohere_client)
- [ ] T012 Create backend/src/models/database.py with SQLAlchemy Base, async engine setup, and session factory using Neon DATABASE_URL from config
- [ ] T013 Create Alembic configuration: `alembic init alembic` and configure sqlalchemy.url to use Neon DATABASE_URL from config
- [ ] T014 Create initial Alembic migration (001_initial_schema.py) with tables: modules, chapters, sections, chunks, question_log, answer_log (per data-model.md)
- [ ] T015 Create backend/src/api/main.py with FastAPI app initialization, CORS middleware, structured logging middleware, and exception handlers
- [ ] T016 [P] Create backend/src/api/middleware/cors.py with CORS configuration for Docusaurus frontend domain
- [ ] T017 [P] Create backend/src/api/middleware/rate_limit.py with slowapi rate limiting (10 req/min for ingestion, 100 req/min for questions)
- [ ] T018 [P] Create backend/src/api/middleware/error_handler.py with consistent JSON error responses (ErrorResponse schema per data-model.md)
- [ ] T019 Create backend/src/api/routes/health.py with GET /api/v1/health endpoint returning status, version, and service health (Qdrant, Neon, Cohere connectivity)
- [ ] T020 Verify foundational setup: Run `uvicorn src.api.main:app --reload` and access http://localhost:8000/api/v1/health successfully

**Acceptance**: FastAPI server runs, health endpoint responds with service statuses, database migrations work, rate limiting active, structured logging captures requests.

---

## Phase 3: User Story 1 - Content Ingestion for RAG System (Priority: P1)

**Story Goal**: Enable system administrators to ingest textbook markdown content, chunk it, generate embeddings, and store in Qdrant + Neon.

**Independent Test**: Provide sample markdown file → verify chunks exist in Qdrant (with embeddings) and Neon (with metadata).

**Acceptance Scenarios** (from spec.md):
1. Markdown file → hierarchical chunks (module → chapter → section) with preserved structure
2. Each chunk → vector embedding in Qdrant with metadata (module, chapter, section, file path)
3. Metadata in Neon → modules, chapters, sections, chunks with parent-child relationships
4. Multiple files → correct hierarchical structure maintained

**Tasks**:

- [ ] T021 [US1] Add SQLAlchemy models to backend/src/models/database.py: Module, Chapter, Section, Chunk (per data-model.md schema)
- [ ] T022 [P] [US1] Create backend/src/models/requests.py with IngestionRequest Pydantic model (file_path, module_title, module_description, module_order)
- [ ] T023 [P] [US1] Create backend/src/models/responses.py with IngestionResponse and IngestionStatusResponse Pydantic models
- [ ] T024 [US1] Create backend/src/utils/markdown_parser.py with function to parse markdown into hierarchical structure (extract headings, identify modules/chapters/sections)
- [ ] T025 [US1] Create backend/src/services/chunker.py with ChunkerService class: chunk_section(text, max_tokens=1024) → list of chunks (split at paragraph boundaries, preserve code blocks)
- [ ] T026 [US1] Create backend/src/services/metadata_store.py with MetadataStoreService class: async methods to create modules, chapters, sections, chunks in Neon (using SQLAlchemy async session)
- [ ] T027 [US1] Create backend/src/services/embedder.py with EmbedderService class: async generate_embedding(text) using Cohere embed-english-v3.0 (handle truncation to 512 tokens)
- [ ] T028 [US1] Create backend/src/services/vector_store.py with VectorStoreService class: async store_chunk(chunk_id, embedding, metadata) to Qdrant, async initialize_collection() to create textbook_chunks collection
- [ ] T029 [US1] Create ingestion orchestration service in backend/src/services/ingestion.py with IngestionService class: async ingest_file(request) → parse markdown, chunk sections, generate embeddings, store in Qdrant + Neon, return job ID
- [ ] T030 [US1] Create backend/src/api/routes/ingestion.py with POST /api/v1/ingestion endpoint (accepts IngestionRequest, returns 202 Accepted with job ID, queues async ingestion job)
- [ ] T031 [US1] Add GET /api/v1/ingestion/status/{job_id} endpoint to backend/src/api/routes/ingestion.py (returns IngestionStatusResponse with job status: accepted, processing, completed, failed)
- [ ] T032 [US1] Mount ingestion routes in backend/src/api/main.py: `app.include_router(ingestion_router, prefix="/api/v1", tags=["Ingestion"])`
- [ ] T033 [US1] Manual integration test: Submit sample markdown file via POST /api/v1/ingestion, verify chunks in Qdrant (query collection) and Neon (SELECT from chunks table), confirm metadata relationships

**Acceptance**: Sample markdown file ingestion completes successfully. Qdrant contains vector embeddings with correct metadata. Neon contains hierarchical structure (modules → chapters → sections → chunks). Status endpoint tracks job progress.

**Parallel Opportunities**:
- T022, T023 (Pydantic models) can run parallel with T024 (markdown parser)
- T026 (metadata store), T027 (embedder), T028 (vector store) are independent services - can implement in parallel
- After T029 completes, T030 and T031 (API routes) can run in parallel

---

## Phase 4: User Story 2 - Full Textbook Question Answering (Priority: P2)

**Story Goal**: Enable learners to ask questions and receive accurate answers with source citations using full textbook retrieval.

**Independent Test**: Submit question via API → verify response includes answer and source citations (module, chapter, section).

**Acceptance Scenarios** (from spec.md):
1. Question → retrieve relevant chunks, generate answer, return with source citations
2. Multi-section question → synthesize answer referencing all relevant sources
3. No relevant content → respond "I cannot answer based on the textbook content"
4. Complex multi-part question → answer addresses all parts with sources

**Tasks**:

- [ ] T034 [P] [US2] Add QuestionRequest Pydantic model to backend/src/models/requests.py (question: str with 5-500 char validation)
- [ ] T035 [P] [US2] Add AnswerResponse and SourceCitation Pydantic models to backend/src/models/responses.py (answer, sources, mode, confidence)
- [ ] T036 [US2] Add QuestionLog SQLAlchemy model to backend/src/models/database.py (question_text, mode, selected_text, user_ip, created_at)
- [ ] T037 [US2] Add AnswerLog SQLAlchemy model to backend/src/models/database.py (question_id FK, answer_text, sources JSONB, retrieved_chunk_ids, model_used, response_time_ms, created_at)
- [ ] T038 [US2] Create backend/src/services/retriever.py with RetrieverService class: async search_similar(query_embedding, top_k=5) → retrieve top-k chunks from Qdrant using cosine similarity
- [ ] T039 [US2] Create backend/src/services/generator.py with GeneratorService class: async generate_answer(question, context_chunks, mode) → use Cohere Command model to generate grounded answer (strict prompting: answer ONLY from context, cite sources)
- [ ] T040 [US2] Create question answering orchestration service in backend/src/services/question.py with QuestionService class: async answer_question(request) → embed question, retrieve chunks, generate answer, log to database, return AnswerResponse
- [ ] T041 [US2] Create backend/src/api/routes/question.py with POST /api/v1/question endpoint (accepts QuestionRequest, returns AnswerResponse)
- [ ] T042 [US2] Mount question routes in backend/src/api/main.py: `app.include_router(question_router, prefix="/api/v1", tags=["Questions"])`
- [ ] T043 [US2] Manual integration test: Ingest sample content (reuse from US1), submit question "What is physical AI?", verify response includes answer + source citations (module, chapter, section), confirm answer is grounded in retrieved chunks

**Acceptance**: Question answering works end-to-end. Responses include accurate answers grounded in textbook content with source citations. No-answer cases return appropriate message. Queries logged to database.

**Parallel Opportunities**:
- T034, T035 (Pydantic models) and T036, T037 (SQLAlchemy models) can run in parallel
- T038 (retriever) and T039 (generator) are independent services - can implement in parallel
- After T040 completes, T041 and T042 (API routes) can run together

---

## Phase 5: User Story 3 - Selected Text Question Answering (Priority: P3)

**Story Goal**: Enable learners to ask questions about user-selected text only (context-restricted mode).

**Independent Test**: Submit question + selected text via API → verify answer uses ONLY selected text (no vector search).

**Acceptance Scenarios** (from spec.md):
1. Question + selected text → answer uses ONLY selected text, marked as context-restricted
2. Insufficient selected text → respond "I cannot answer based on the selected text alone"
3. Response clearly indicates context-restricted mode

**Tasks**:

- [ ] T044 [P] [US3] Add SelectedTextQuestionRequest Pydantic model to backend/src/models/requests.py (question: str, selected_text: str with 10-5000 char validation)
- [ ] T045 [US3] Extend backend/src/services/question.py QuestionService with async answer_selected_text(request) → generate answer using ONLY selected_text as context (no vector search), return AnswerResponse with mode="selected_text"
- [ ] T046 [US3] Add POST /api/v1/question/selected-text endpoint to backend/src/api/routes/question.py (accepts SelectedTextQuestionRequest, returns AnswerResponse)
- [ ] T047 [US3] Manual integration test: Submit question + selected text via POST /api/v1/question/selected-text, verify answer is generated from selected text only (no other sources cited), confirm mode="selected_text" in response

**Acceptance**: Selected text mode works independently. Answers strictly limited to provided text. Response clearly marked as context-restricted.

**Parallel Opportunities**:
- T044 (Pydantic model) can run while implementing T045 (service logic)
- T046 (API route) immediately follows T045

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Add production-ready polish (input validation, comprehensive error handling, performance monitoring, OpenAPI docs)

**Tasks**:

- [ ] T048 [P] Create backend/src/utils/validators.py with input validation functions (validate question length, sanitize markdown, validate file paths)
- [ ] T049 [P] Add request validation middleware to backend/src/api/middleware/error_handler.py (catch Pydantic validation errors, return 400 with clear messages)
- [ ] T050 [P] Add comprehensive error handling in all service classes (catch Cohere API errors, Qdrant connection errors, Neon database errors, return structured errors)
- [ ] T051 [P] Add response time tracking in backend/src/api/main.py middleware (log request duration, store in AnswerLog.response_time_ms)
- [ ] T052 [P] Verify OpenAPI documentation: Access http://localhost:8000/docs and confirm all endpoints match contracts/openapi.yaml (request/response schemas, descriptions, examples)
- [ ] T053 [P] Add edge case handling in backend/src/services/chunker.py (malformed markdown, missing headings, very long code blocks)
- [ ] T054 [P] Add edge case handling in backend/src/services/generator.py (very long questions, special characters, non-English text)
- [ ] T055 [P] Add graceful degradation in backend/src/api/routes/health.py (return "degraded" if Qdrant/Neon/Cohere unavailable, still return 200 OK)
- [ ] T056 Run full manual test suite covering all user stories and edge cases (ingestion, full textbook Q&A, selected text Q&A, rate limiting, error cases)

**Acceptance**: All edge cases handled gracefully. Errors return clear messages. OpenAPI docs accurate. Performance metrics logged. System degrades gracefully when services unavailable.

**Parallel Opportunities**: All tasks in this phase (T048-T055) can run in parallel as they touch different files/concerns.

---

## User Story Dependencies

### Completion Order

```
Phase 1 (Setup) → Phase 2 (Foundational)
                       ↓
                   Phase 3 (US1 - Ingestion) [REQUIRED FIRST]
                       ↓
                   Phase 4 (US2 - Full Textbook Q&A) [Depends on US1 for ingested content]
                       ↓
                   Phase 5 (US3 - Selected Text Q&A) [Independent of US2, but uses same answer generation infrastructure]
                       ↓
                   Phase 6 (Polish)
```

**Key Dependencies**:
- **US2 requires US1**: Cannot answer questions without ingested content
- **US3 is independent of US2**: Selected text mode doesn't use vector search, but shares answer generation service
- **MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1) = Minimum viable product (content ingestion works)
- **Core Value**: Add Phase 4 (US2) for full textbook question answering (primary user-facing feature)
- **Enhanced UX**: Add Phase 5 (US3) for selected text mode (nice-to-have)

### Parallel Execution Examples

**Within US1 (Ingestion)**:
```bash
# Can run in parallel after T021 completes:
- T022 (IngestionRequest model) || T023 (IngestionResponse model) || T024 (markdown parser)

# Can run in parallel after T024 completes:
- T026 (metadata store) || T027 (embedder) || T028 (vector store)

# Can run in parallel after T029 completes:
- T030 (ingestion endpoint) || T031 (status endpoint)
```

**Within US2 (Question Answering)**:
```bash
# Can run in parallel:
- T034 (QuestionRequest) || T035 (AnswerResponse) || T036 (QuestionLog model) || T037 (AnswerLog model)

# Can run in parallel after models complete:
- T038 (retriever service) || T039 (generator service)
```

**Within US3 (Selected Text)**:
```bash
# Can run in parallel:
- T044 (SelectedTextQuestionRequest) || T045 (selected text service logic)
```

---

## Implementation Strategy

### MVP First (Recommended)

**Phase 1 → Phase 2 → Phase 3** = MVP (Content ingestion works)

Complete ingestion first to establish the foundational RAG capability. This enables:
- Testing with real textbook content
- Validating chunking strategy (1024 tokens)
- Verifying Qdrant + Neon integration
- Debugging embedding generation

**Benefits**:
- Quick validation of core RAG pipeline
- Early feedback on chunking quality
- Foundation for all subsequent features

### Incremental Delivery

**MVP + Phase 4** = Core Value (Question answering works)

After MVP, add full textbook question answering (US2) to deliver primary user-facing value:
- Learners can ask questions
- Answers include source citations
- Grounded generation prevents hallucinations

**MVP + Phase 4 + Phase 5** = Enhanced UX

Finally, add selected text mode (US3) for focused learning experience:
- Context-restricted answers
- No irrelevant retrieval
- Clearer explanations for specific passages

### Testing Strategy

**After Each Phase**:
1. Run manual integration tests (T033, T043, T047)
2. Verify independent test criteria (spec.md acceptance scenarios)
3. Confirm phase is complete before moving to next

**After Phase 6**:
1. Run full test suite (T056)
2. Validate all edge cases
3. Verify OpenAPI docs match implementation
4. Check performance metrics

---

## Task Summary

**Total Tasks**: 56
**Setup & Foundational**: 20 tasks (T001-T020)
**US1 (Ingestion)**: 13 tasks (T021-T033)
**US2 (Question Answering)**: 10 tasks (T034-T043)
**US3 (Selected Text)**: 4 tasks (T044-T047)
**Polish**: 9 tasks (T048-T056)

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel

**Independent Test Points**:
- ✅ Phase 3 (US1): Ingest sample file → verify chunks in Qdrant + Neon
- ✅ Phase 4 (US2): Ask question → verify answer + sources
- ✅ Phase 5 (US3): Ask about selected text → verify context-restricted answer

**MVP Scope**: Tasks T001-T033 (33 tasks) = Minimum viable product
**Core Value**: Add T034-T043 (10 tasks) = Full textbook Q&A
**Enhanced UX**: Add T044-T047 (4 tasks) = Selected text mode
**Production-Ready**: Add T048-T056 (9 tasks) = Polish & edge cases

---

**Ready for Implementation**: Start with Phase 1 (Project Setup) and proceed sequentially through phases. Use parallel execution opportunities within each phase to maximize velocity.