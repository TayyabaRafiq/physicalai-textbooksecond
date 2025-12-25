<!--
Sync Impact Report:
- Version: Initial (none) → 1.0.0
- Changes: Initial constitution creation for AI-driven Physical AI Textbook RAG Chatbot Backend
- Added sections: All sections (initial creation)
- Templates status:
  ✅ .specify/templates/plan-template.md (reviewed - compatible)
  ✅ .specify/templates/spec-template.md (reviewed - compatible)
  ✅ .specify/templates/tasks-template.md (reviewed - compatible)
- Follow-up: None
- Date: 2025-12-21
-->

# AI-driven Physical AI Textbook – Integrated RAG Chatbot Backend Constitution

## Purpose

Design and implement a backend system that enables a Retrieval-Augmented Generation (RAG) chatbot embedded within a published Docusaurus-based Physical AI textbook. The chatbot must answer user questions strictly based on textbook content or user-selected text.

## Core Principles

### I. Spec-Driven Development

All features, APIs, and systems MUST originate from written specifications before implementation.

- Specifications are the single source of truth for the backend
- No code is written without a corresponding spec in `specs/` directory
- Specifications MUST be reviewed and approved before implementation begins
- Changes to scope require specification updates first

**Rationale**: Spec-driven development ensures clarity, prevents ad-hoc implementation, and maintains architectural integrity across the backend system.

### II. Clear Separation of Concerns

The backend MUST remain strictly separate from frontend logic and presentation.

- Backend is a pure REST API service
- No frontend logic or templates in backend code
- Frontend (Docusaurus static site) consumes backend via API calls only
- Backend is frontend-agnostic and could serve multiple clients

**Rationale**: Separation enables independent deployment, testing, and evolution of backend and frontend systems.

### III. Source-Grounded Answers Only

The chatbot MUST NEVER hallucinate or generate content beyond retrieved textbook chunks.

- All answers MUST reference specific retrieved content
- Responses include source citations (module, chapter, section)
- If no relevant content is found, respond with "I cannot answer based on the textbook content"
- No general knowledge responses outside textbook scope

**Rationale**: Grounding ensures accuracy, builds user trust, and aligns with educational integrity principles.

### IV. Beginner-Friendly Explanations

The chatbot MUST provide explanations accessible to learners without advanced AI or robotics knowledge.

- Responses prioritize clarity over technical complexity
- Complex terms are explained when used
- Examples are practical and directly relevant
- Tone is supportive and educational

**Rationale**: Aligns with the textbook's mission to welcome learners from diverse backgrounds into Physical AI and robotics.

### V. Production-Ready, Scalable Architecture

The backend MUST be designed for cloud deployment with scalability in mind.

- Stateless API design for horizontal scaling
- Configuration via environment variables only
- Database migrations managed via version control
- API rate limiting and error handling from day one
- Deployment-ready for Railway / Render / Fly.io

**Rationale**: Production-ready architecture ensures the system is not just a prototype but a functional, deployable learning platform.

## Technology Stack

All implementation MUST use the specified technologies without deviation.

**Backend Framework**: FastAPI (Python)
- RESTful API endpoints
- Automatic OpenAPI documentation
- Async support for I/O-bound operations

**Embedding & LLM Provider**: Cohere models
- `embed-english-v3.0` for text embeddings
- Cohere Command models for answer generation
- NO OpenAI API dependency

**Vector Database**: Qdrant Cloud (Free Tier)
- Vector storage for textbook embeddings
- Similarity search for retrieval
- Managed cloud service (no self-hosting)

**Relational Database**: Neon Serverless Postgres
- Metadata storage (modules, chapters, sections, sources)
- Query logging and analytics
- Serverless, autoscaling

**Deployment Target**: Cloud-ready
- Compatible with Railway / Render / Fly.io
- Environment-based configuration
- No vendor lock-in

**Frontend Integration**: Docusaurus static site
- Backend consumed via REST API calls
- CORS configured for static site domain
- No server-side rendering dependencies

**Rationale**: These technologies provide free/low-cost deployment, proven scalability, and align with modern cloud-native best practices.

## Key Capabilities

The backend MUST provide the following capabilities:

### 1. Content Ingestion
- Ingest textbook markdown content from filesystem or API
- Parse markdown into structured chunks (sections, subsections)
- Extract metadata (module, chapter, section titles, hierarchy)

### 2. Chunk and Embed
- Chunk textbook content into semantically meaningful units
- Generate embeddings using Cohere `embed-english-v3.0`
- Store embeddings in Qdrant with metadata

### 3. Metadata Storage
- Store module, chapter, section structure in Neon Postgres
- Link chunks to source locations (file, heading, line range)
- Enable source attribution in chatbot responses

### 4. Question Answering - Full Textbook Mode
- Accept user question as input
- Retrieve relevant chunks from Qdrant via vector similarity
- Generate answer using Cohere Command model with retrieved context
- Return answer with source citations

### 5. Question Answering - Selected Text Mode
- Accept user question + user-selected text as input
- Restrict context to ONLY the selected text
- Generate answer using Cohere Command model with selected text
- Return answer clearly marked as context-restricted

### 6. Strict Grounding
- All responses MUST reference retrieved chunks
- Include source metadata (module, chapter, section, file) in responses
- Reject questions when no relevant content is found
- No general knowledge responses outside textbook scope

### 7. Rate Limiting and Safety
- Rate limit API endpoints to prevent abuse
- Validate and sanitize user inputs
- Handle errors gracefully with clear messages
- Log queries for monitoring and improvement

## Constraints

The following constraints MUST be respected:

- **NO OpenAI APIs**: All embedding and generation MUST use Cohere
- **Cohere API ONLY**: Use Cohere for embeddings (`embed-english-v3.0`) and generation (Command models)
- **Qdrant Cloud REQUIRED**: Vector storage via Qdrant Cloud endpoint and API key
- **Neon Database REQUIRED**: Relational storage via Neon database URL
- **No Frontend Logic**: Backend is pure API, no templates or UI
- **Environment Variables ONLY**: All configuration via `.env` (NEVER hardcoded)
- **No Secrets in Repo**: API keys and credentials MUST be excluded from version control

## Required Environment Variables

The following environment variables MUST be configured for the backend to function:

```
COHERE_API_KEY=<your-cohere-api-key>
QDRANT_API_KEY=<your-qdrant-api-key>
QDRANT_URL=<your-qdrant-cluster-url>
QDRANT_CLUSTER_ID=<your-qdrant-cluster-id>
NEON_DATABASE_URL=<your-neon-postgres-connection-string>
```

All sensitive values MUST be stored in `.env` and NEVER committed to the repository. A `.env.example` template MUST be provided with placeholder values.

## Success Criteria

The backend project achieves its goals when:

1. **End-to-End Content Ingestion**: Backend can ingest textbook markdown content, chunk it, embed it, and store it in Qdrant and Neon
2. **Accurate, Grounded Answers**: Chatbot answers are based solely on retrieved textbook content with source citations
3. **Selected-Text Mode Works**: Users can ask questions about selected text, and answers are strictly limited to that context
4. **Clean API Contract**: API endpoints are well-documented, consistent, and ready for frontend integration
5. **Fully Specified Before Implementation**: All features are defined via specs before any code is written
6. **Production-Ready**: Backend is deployable to cloud platforms with proper configuration and error handling

## Explicit Non-Goals

This backend does NOT aim to:

- **Implement Frontend UI**: Frontend is handled by Docusaurus (separate concern)
- **Use OpenAI APIs**: Cohere is the exclusive provider for embeddings and generation
- **Self-Host Infrastructure**: Use managed cloud services (Qdrant Cloud, Neon) instead
- **Provide General AI Capabilities**: Strictly limited to textbook-based question answering
- **Optimize for Multi-Tenancy**: Single textbook, single deployment focus

## Development Workflow

### Specification Process

1. Feature or API requirements are documented in `specs/<feature>/spec.md`
2. Specifications include user stories, API contracts, and success criteria
3. AI (Claude Code) assists in specification refinement and validation
4. Specifications are reviewed before implementation begins

### Implementation Process

1. Implementation plans are created in `specs/<feature>/plan.md`
2. Tasks are broken down in `specs/<feature>/tasks.md`
3. Implementation follows TDD principles where applicable (unit tests, integration tests)
4. All significant changes are tracked via PHRs in `history/prompts/`

### Architectural Decisions

When architecturally significant decisions are made:
- The decision MUST be documented in `history/adr/`
- ADRs capture context, options considered, and rationale
- ADRs are suggested during planning, never auto-created
- Suggestion format: "📋 Architectural decision detected: [brief] — Document reasoning? Run `/sp.adr <title>`"

## Quality Standards

### API Quality

- All endpoints follow RESTful conventions (proper HTTP verbs, status codes)
- Request/response schemas are validated with Pydantic models
- Errors return consistent JSON structure with clear messages
- API documentation is auto-generated via FastAPI OpenAPI

### Code Quality

- Follow PEP 8 style guidelines for Python code
- Type hints for all function signatures
- Docstrings for public functions and classes
- Unit tests for core logic, integration tests for API endpoints

### RAG Quality

- Retrieved chunks are semantically relevant to user questions
- Answers cite specific sources accurately (module, chapter, section)
- Selected-text mode strictly limits context to provided text
- Response latency is acceptable for interactive learning (<3 seconds)

### Security

- API keys and credentials stored in environment variables only
- Input validation and sanitization for all user inputs
- Rate limiting to prevent abuse
- CORS configured for allowed frontend domains only

## Governance

### Constitution Authority

This constitution supersedes all other backend practices and guidelines. When conflicts arise, constitution principles take precedence.

### Amendment Process

1. Proposed changes are documented with rationale
2. Changes are reviewed for impact on existing specifications and implementations
3. Dependent templates and documentation are updated to maintain consistency
4. Version is incremented according to semantic versioning rules
5. Sync Impact Report is generated and included in the constitution file

### Versioning Policy

- **MAJOR**: Backward-incompatible principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance

- All specifications MUST reference and comply with relevant principles
- Implementation plans MUST include "Constitution Check" sections
- Pull requests MUST verify compliance with applicable principles
- Violations MUST be justified and documented in complexity tracking tables

**Version**: 1.0.0 | **Ratified**: 2025-12-21 | **Last Amended**: 2025-12-21