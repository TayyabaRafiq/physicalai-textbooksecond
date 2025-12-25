# Implementation Plan: RAG Chatbot Backend – Core Question Answering Pipeline

**Branch**: `001-rag-chatbot-pipeline` | **Date**: 2025-12-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot-pipeline/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Retrieval-Augmented Generation (RAG) backend system that enables a chatbot to answer learner questions about the Physical AI textbook. The system ingests textbook markdown content, chunks it into semantically meaningful units (1024 tokens), generates vector embeddings using Cohere embed-english-v3.0, stores embeddings in Qdrant Cloud and metadata in Neon Postgres, and exposes REST API endpoints for question answering in two modes: (1) full textbook retrieval and (2) user-selected text only (context-restricted). All answers must include source citations and be grounded in retrieved content to prevent hallucinations.

**Technical Approach**: FastAPI-based REST API with async I/O, Cohere SDK for embeddings and generation, Qdrant Python client for vector operations, SQLAlchemy for Neon Postgres ORM, Pydantic for request/response validation, and environment-based configuration.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.104+, Cohere Python SDK 4.x+, Qdrant Client 1.7+, SQLAlchemy 2.0+, Pydantic 2.x+, Uvicorn (ASGI server), python-dotenv (environment management)
**Storage**: Qdrant Cloud (vector embeddings), Neon Serverless Postgres (metadata)
**Testing**: pytest 7.x+, pytest-asyncio (async test support), httpx (API testing), pytest-cov (coverage)
**Target Platform**: Linux server (Railway / Render / Fly.io compatible), containerized deployment (Docker)
**Project Type**: Single backend API project (backend/ directory in monorepo)
**Performance Goals**: <3s response time for 95% of queries, <5min ingestion for 50+ page module, 100+ concurrent requests supported
**Constraints**: <200ms p95 for embedding generation, <500ms p95 for vector similarity search, stateless API design (no session state), environment-variable-only configuration
**Scale/Scope**: Single textbook (~500-1000 chunks), 100+ concurrent users, 10k+ questions per day

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate (Initial Check)

- ✅ **Spec-Driven Development (I)**: Implementation plan follows approved specification in specs/001-rag-chatbot-pipeline/spec.md
- ✅ **Clear Separation of Concerns (II)**: Backend is pure REST API with no frontend logic
- ✅ **Source-Grounded Answers Only (III)**: Architecture ensures all answers reference retrieved chunks (FR-013)
- ✅ **Beginner-Friendly Explanations (IV)**: Prompting strategy will enforce accessible language in generated answers
- ✅ **Production-Ready, Scalable Architecture (V)**: Stateless API, environment-based config, rate limiting from day one
- ✅ **Technology Stack Adherence**: FastAPI, Cohere (NO OpenAI), Qdrant Cloud, Neon Postgres as mandated
- ✅ **Required Environment Variables**: All secrets (COHERE_API_KEY, QDRANT_API_KEY, QDRANT_URL, NEON_DATABASE_URL) configured via .env

**Gate Status**: ✅ PASSED - Proceed to Phase 0 research

### Post-Design Gate (After Phase 1)

- ✅ **Spec-Driven Development (I)**: All Phase 1 artifacts (research.md, data-model.md, contracts/openapi.yaml, quickstart.md) generated and align with specification
- ✅ **Clear Separation of Concerns (II)**: Data model enforces separation (Neon for metadata, Qdrant for vectors, no frontend coupling)
- ✅ **Source-Grounded Answers Only (III)**: API contract ensures source citations in AnswerResponse schema, Qdrant payload stores chunk content for grounding validation
- ✅ **Beginner-Friendly Explanations (IV)**: OpenAPI documentation uses clear language, quickstart provides step-by-step onboarding
- ✅ **Production-Ready, Scalable Architecture (V)**: Research decisions validate stateless design, rate limiting (slowapi), structured logging, async I/O patterns
- ✅ **Technology Stack Adherence**: All research and data model decisions use mandated technologies (FastAPI, Cohere, Qdrant, Neon)
- ✅ **Required Environment Variables**: quickstart.md documents all required env vars, .env.example template provided

**Gate Status**: ✅ PASSED - Design artifacts complete and compliant with constitution

**Artifacts Generated**:
- research.md (Phase 0): Technology decisions, best practices, architectural patterns
- data-model.md (Phase 1): Neon Postgres schema, Qdrant collection, Pydantic models
- contracts/openapi.yaml (Phase 1): Complete REST API specification
- quickstart.md (Phase 1): Developer onboarding guide
- Agent context updated: CLAUDE.md includes Python 3.11+, FastAPI, Cohere, Qdrant, Neon

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-pipeline/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - technology decisions and patterns
├── data-model.md        # Phase 1 output - database schema and entities
├── quickstart.md        # Phase 1 output - developer getting started guide
├── contracts/           # Phase 1 output - API contracts
│   └── openapi.yaml     # OpenAPI 3.0 specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/                  # FastAPI application and routes
│   │   ├── main.py           # FastAPI app initialization
│   │   ├── routes/           # API endpoint definitions
│   │   │   ├── ingestion.py  # Content ingestion endpoints
│   │   │   ├── question.py   # Question answering endpoints
│   │   │   └── health.py     # Health check and status
│   │   └── middleware/       # CORS, rate limiting, error handling
│   │       ├── cors.py
│   │       ├── rate_limit.py
│   │       └── error_handler.py
│   ├── models/               # Data models and schemas
│   │   ├── database.py       # SQLAlchemy models (Neon Postgres)
│   │   ├── requests.py       # Pydantic request schemas
│   │   └── responses.py      # Pydantic response schemas
│   ├── services/             # Business logic layer
│   │   ├── chunker.py        # Markdown parsing and chunking
│   │   ├── embedder.py       # Cohere embedding generation
│   │   ├── vector_store.py   # Qdrant client wrapper
│   │   ├── metadata_store.py # Neon Postgres client wrapper
│   │   ├── retriever.py      # Vector similarity search
│   │   └── generator.py      # Cohere answer generation
│   ├── core/                 # Core utilities and configuration
│   │   ├── config.py         # Environment-based configuration
│   │   ├── logging.py        # Structured logging setup
│   │   └── dependencies.py   # FastAPI dependency injection
│   └── utils/                # Helper functions
│       ├── markdown_parser.py
│       └── validators.py
├── tests/
│   ├── unit/                 # Unit tests for services and utils
│   │   ├── test_chunker.py
│   │   ├── test_embedder.py
│   │   └── test_generator.py
│   ├── integration/          # Integration tests for API endpoints
│   │   ├── test_ingestion_api.py
│   │   └── test_question_api.py
│   └── contract/             # API contract tests (OpenAPI validation)
│       └── test_openapi_compliance.py
├── .env.example              # Environment variable template
├── .gitignore                # Excludes .env, __pycache__, etc.
├── pyproject.toml            # Python project metadata and dependencies
├── README.md                 # Project overview and setup
└── Dockerfile                # Container image for deployment
```

**Structure Decision**: Single backend API project within the backend/ directory of the monorepo. This structure follows FastAPI best practices with clear separation between API layer (routes), business logic (services), data models, and core configuration. The src/ layout enables clean imports and testability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations identified. All constitutional requirements are satisfied:
- Technology stack adheres to mandated choices (FastAPI, Cohere, Qdrant, Neon)
- No frontend logic in backend
- Source grounding enforced architecturally
- Production-ready patterns (stateless, env-based config, rate limiting) from day one

---

**Phase 0 Status**: ✅ COMPLETED - research.md generated with all technical decisions
**Phase 1 Status**: ✅ COMPLETED - data-model.md, contracts/openapi.yaml, quickstart.md generated
**Phase 2 Status**: Pending (will be handled by /sp.tasks command)

**Ready for**: `/sp.tasks` to generate task breakdown for implementation