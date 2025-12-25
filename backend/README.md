# AI-driven Physical AI Textbook - RAG Chatbot Backend

This is the backend system for the integrated RAG (Retrieval-Augmented Generation) chatbot embedded within the Physical AI & Humanoid Robotics textbook.

## Purpose

Provide a REST API that enables:
- Textbook content ingestion and embedding
- Vector similarity search using Qdrant
- Question answering based on textbook content (full textbook or selected text)
- Strict source grounding with citation support

## Technology Stack

- **Framework**: FastAPI (Python)
- **Embeddings & LLM**: Cohere models (embed-english-v3.0, Command)
- **Vector Database**: Qdrant Cloud (Free Tier)
- **Relational Database**: Neon Serverless Postgres
- **Deployment**: Railway / Render / Fly.io compatible

## Project Structure

This backend follows **Spec-Driven Development** using Spec-Kit Plus:

- `.specify/` - Templates, scripts, and project constitution
- `specs/` - Feature specifications, plans, and tasks
- `history/` - Prompt History Records (PHRs) and Architecture Decision Records (ADRs)

## Constitution

See `.specify/memory/constitution.md` for the complete project constitution, which defines:
- Core principles (spec-driven, separation of concerns, source-grounded answers)
- Technology stack requirements
- Quality standards
- Development workflow

## Getting Started

**IMPORTANT**: This project is currently in the specification phase. No implementation code should be written until specifications are complete.

### Next Steps

1. Review the constitution: `.specify/memory/constitution.md`
2. Create feature specifications using `/sp.specify`
3. Generate implementation plans using `/sp.plan`
4. Break down into tasks using `/sp.tasks`
5. Only then begin implementation using `/sp.implement`

### Environment Setup (for future implementation)

1. Copy `.env.example` to `.env`
2. Fill in your API keys and connection strings:
   - Cohere API key (get from https://cohere.com)
   - Qdrant Cloud credentials (get from https://qdrant.tech)
   - Neon database URL (get from https://neon.tech)
3. Never commit `.env` to version control

## Constraints

- **NO OpenAI APIs** - Only Cohere models
- **NO frontend logic** - Pure REST API
- **NO hardcoded secrets** - Environment variables only
- **NO implementation without specs** - Spec-driven only

## Documentation

- Constitution: `.specify/memory/constitution.md`
- Specifications: `specs/<feature>/spec.md`
- Implementation Plans: `specs/<feature>/plan.md`
- Tasks: `specs/<feature>/tasks.md`
- ADRs: `history/adr/`
- PHRs: `history/prompts/`

---

**Version**: 1.0.0 | **Status**: Specification Phase | **Created**: 2025-12-21
