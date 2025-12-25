# Feature Specification: RAG Chatbot Backend – Core Question Answering Pipeline

**Feature Branch**: `001-rag-chatbot-pipeline`
**Created**: 2025-12-21
**Status**: Draft
**Input**: User description: "Feature: RAG Chatbot Backend – Core Question Answering Pipeline

Description:
Specify the core backend feature that enables a Retrieval-Augmented Generation (RAG) chatbot for the Physical AI textbook.

This feature defines how textbook content is ingested, embedded, stored, retrieved, and used to answer learner questions through an API.

Scope:
This specification covers ONLY behavior and requirements.
No implementation details or code.

Functional Requirements:
1. Accept textbook markdown files as input
2. Chunk content by module, chapter, and section
3. Generate embeddings using Cohere models
4. Store embeddings in Qdrant with metadata references
5. Store structural metadata in Neon Postgres
6. Expose an API endpoint to:
   - Answer questions using full textbook retrieval
   - Answer questions using user-selected text only (context-restricted mode)
7. Return answers that include:
   - The generated answer
   - Source references (module/chapter/section)
8. Reject or safely respond to questions when no relevant content is found

Non-Functional Requirements:
- No hallucinations: answers must be grounded in retrieved chunks
- Stateless API design
- Safe for public access (rate limiting supported)
- Environment-variable–only configuration

Out of Scope:
- Frontend UI
- Authentication
- Payments
- Analytics dashboards

Success Criteria:
- All requirements are testable
- Clear separation between ingestion and query phases
- API contract ready for frontend integration"

## User Scenarios & Testing

### User Story 1 - Content Ingestion for RAG System (Priority: P1)

As a system administrator, I need to ingest the Physical AI textbook markdown content into the RAG system so that the chatbot has a knowledge base to answer learner questions from.

**Why this priority**: Without ingested content, the chatbot cannot answer any questions. This is the foundational capability that enables all other features.

**Independent Test**: Can be fully tested by providing sample markdown files and verifying that content is chunked, embedded, and stored in both Qdrant (embeddings) and Neon (metadata). Success means querying the databases confirms the presence of chunked content with proper metadata.

**Acceptance Scenarios**:

1. **Given** a markdown file representing a textbook module with chapters and sections, **When** the ingestion process runs, **Then** the content is parsed into hierarchical chunks (module → chapter → section) with preserved structure
2. **Given** chunked textbook content, **When** embeddings are generated, **Then** each chunk has a corresponding vector embedding stored in Qdrant with metadata linking back to its source (module, chapter, section, file path)
3. **Given** chunked textbook content, **When** metadata is stored, **Then** Neon Postgres contains records for each module, chapter, section, and chunk with proper parent-child relationships
4. **Given** multiple markdown files ingested, **When** querying metadata, **Then** the system correctly maintains the hierarchical structure and source attribution for all content

---

### User Story 2 - Full Textbook Question Answering (Priority: P2)

As a learner reading the Physical AI textbook, I want to ask questions about any topic covered in the book and receive accurate answers with source citations so that I can deepen my understanding without searching manually.

**Why this priority**: This is the primary user-facing value of the RAG chatbot - enabling learners to ask questions and get answers grounded in the textbook content.

**Independent Test**: Can be tested by submitting questions via API and verifying that responses include both a relevant answer and source citations. Success means the answer accurately reflects textbook content and cites the correct module/chapter/section.

**Acceptance Scenarios**:

1. **Given** the textbook content has been ingested, **When** a learner asks "What is physical AI?", **Then** the system retrieves relevant chunks from Qdrant, generates an answer using Cohere, and returns the answer with source citations (e.g., "Module 1, Chapter 1, Section 2")
2. **Given** a question that matches content across multiple sections, **When** the question is processed, **Then** the system retrieves the most relevant chunks and synthesizes an answer that references all relevant sources
3. **Given** a question with no relevant content in the textbook, **When** the question is processed, **Then** the system responds with "I cannot answer based on the textbook content" without hallucinating or providing general knowledge
4. **Given** a complex multi-part question, **When** the system processes it, **Then** the answer addresses all parts and cites sources for each claim made

---

### User Story 3 - Selected Text Question Answering (Priority: P3)

As a learner reading a specific section of the textbook, I want to select text and ask questions about only that selected text so that I can get focused explanations without irrelevant context from other parts of the book.

**Why this priority**: This provides a more focused learning experience and prevents the chatbot from pulling in unrelated content when the learner wants clarification on a specific passage.

**Independent Test**: Can be tested by providing both a question and selected text via API, then verifying the answer is generated using only the selected text as context. Success means the response clearly indicates it's context-restricted and doesn't reference other textbook sections.

**Acceptance Scenarios**:

1. **Given** a learner selects a paragraph about "humanoid robot perception" and asks "How does this work?", **When** the question is processed in selected-text mode, **Then** the system generates an answer using ONLY the selected text and marks the response as context-restricted
2. **Given** selected text that doesn't contain enough information to answer the question, **When** the system processes the question, **Then** it responds with "I cannot answer based on the selected text alone" without retrieving additional content from the textbook
3. **Given** a question about the selected text, **When** the answer is generated, **Then** the response includes a clear indicator that it's based only on the selected text (not the full textbook)

---

### Edge Cases

- What happens when the same question is asked repeatedly (rate limiting, caching)?
- How does the system handle malformed markdown during ingestion (missing headings, broken structure)?
- What happens when a question contains special characters, code blocks, or non-English text?
- How does the system behave when Qdrant or Neon is temporarily unavailable?
- What happens when embedding generation fails for a chunk (network error, API limit)?
- How does the system handle very long questions (token limits) or very short questions (ambiguous intent)?
- What happens when selected text is empty or extremely long (beyond model context window)?
- How does the system handle concurrent ingestion requests (same content ingested multiple times)?

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept markdown files as input for content ingestion
- **FR-002**: System MUST parse markdown files into hierarchical chunks based on heading structure (module/chapter/section)
- **FR-003**: System MUST generate vector embeddings for each chunk using Cohere embed-english-v3.0 model
- **FR-004**: System MUST store vector embeddings in Qdrant Cloud with metadata (chunk ID, source file, module, chapter, section)
- **FR-005**: System MUST store structural metadata in Neon Postgres (modules, chapters, sections, chunks) with parent-child relationships
- **FR-006**: System MUST provide a REST API endpoint for full textbook question answering that accepts a question string and returns an answer with source citations
- **FR-007**: System MUST provide a REST API endpoint for selected-text question answering that accepts a question string and selected text, returning an answer based only on the selected text
- **FR-008**: System MUST retrieve relevant chunks from Qdrant using vector similarity search for full textbook mode
- **FR-009**: System MUST generate answers using Cohere Command model with retrieved chunks as context
- **FR-010**: System MUST include source citations (module, chapter, section) in all answers
- **FR-011**: System MUST respond with "I cannot answer based on the textbook content" when no relevant content is found (full textbook mode)
- **FR-012**: System MUST respond with "I cannot answer based on the selected text alone" when selected text is insufficient (selected-text mode)
- **FR-013**: System MUST NOT generate answers using knowledge outside the retrieved textbook chunks (no hallucinations)
- **FR-014**: System MUST support rate limiting on API endpoints to prevent abuse
- **FR-015**: System MUST validate and sanitize all user inputs (questions, selected text)
- **FR-016**: System MUST load all configuration from environment variables (API keys, database URLs)
- **FR-017**: System MUST return structured JSON responses with consistent error handling
- **FR-018**: System MUST log all questions and answers for monitoring and improvement
- **FR-019**: System MUST handle chunking strategy that preserves semantic meaning (default: section-level chunks with target chunk size of 1024 tokens per chunk for balanced context preservation and retrieval precision)
- **FR-020**: System MUST support CORS configuration for frontend domain integration

### Key Entities

- **TextbookModule**: Represents a top-level module in the textbook (e.g., "Module 1: Introduction to Physical AI"). Attributes: module ID, title, description, order. Relationships: contains multiple chapters.
- **TextbookChapter**: Represents a chapter within a module (e.g., "Chapter 1: What is Physical AI?"). Attributes: chapter ID, title, module ID (parent), order. Relationships: belongs to one module, contains multiple sections.
- **TextbookSection**: Represents a section within a chapter (e.g., "Section 1.1: Defining Physical AI"). Attributes: section ID, title, chapter ID (parent), order. Relationships: belongs to one chapter, contains multiple chunks.
- **TextbookChunk**: Represents a semantically meaningful piece of content for RAG retrieval. Attributes: chunk ID, content (text), section ID (parent), file path, line range, embedding ID (reference to Qdrant vector). Relationships: belongs to one section.
- **Question**: Represents a user question submitted to the chatbot. Attributes: question ID, question text, mode (full_textbook | selected_text), selected text (if applicable), timestamp, user IP (for rate limiting). Relationships: produces one answer.
- **Answer**: Represents a generated answer to a question. Attributes: answer ID, question ID, answer text, source citations (list of module/chapter/section references), retrieved chunks (list of chunk IDs), timestamp, model used. Relationships: belongs to one question.

## Success Criteria

### Measurable Outcomes

- **SC-001**: System can ingest a complete textbook module (50+ pages of markdown) and chunk, embed, and store all content in under 5 minutes
- **SC-002**: Question answering API returns responses (answer + sources) in under 3 seconds for 95% of queries
- **SC-003**: System achieves 90%+ grounding accuracy - meaning 90% of generated answers cite only content present in the retrieved chunks (verified by human evaluation on sample questions)
- **SC-004**: System correctly rejects questions with no relevant content 95%+ of the time (no hallucinations when knowledge is unavailable)
- **SC-005**: Selected-text mode answers are restricted to the provided text 100% of the time (no external retrieval)
- **SC-006**: API endpoints support at least 100 concurrent requests without degradation
- **SC-007**: System handles rate limiting gracefully, returning clear error messages when limits are exceeded
- **SC-008**: Source citations are accurate 95%+ of the time - cited module/chapter/section actually contains the information in the answer
- **SC-009**: Learners can successfully get answers to common textbook questions (tested with 50 sample questions covering all modules) with 85%+ satisfaction rate
- **SC-010**: API contract is complete and unambiguous, enabling frontend integration without backend changes

## Assumptions

- Textbook markdown files follow a consistent heading structure (# for modules, ## for chapters, ### for sections)
- Each markdown file represents one module or a well-defined portion of the textbook
- The Cohere embed-english-v3.0 model produces embeddings suitable for semantic similarity in educational content
- Qdrant Cloud Free Tier provides sufficient storage and query performance for a single textbook (estimated ~500-1000 chunks)
- Neon Serverless Postgres provides sufficient storage for metadata (~10,000 records max)
- Target chunk size of 1024 tokens balances retrieval precision and context completeness (as specified in FR-019)
- Rate limiting defaults to 100 requests per minute per IP address (configurable via environment variable)
- Frontend will handle user authentication and session management (backend is stateless)
- CORS will be configured to allow requests from a specific Docusaurus static site domain

## Out of Scope

- Frontend UI components (handled by Docusaurus)
- User authentication and authorization (backend is stateless, assumes frontend handles auth)
- Payment processing or subscription management
- Analytics dashboards or admin panels
- Multi-language support (English-only for MVP)
- Real-time content updates (ingestion is a batch process, not live sync)
- User feedback mechanisms (like/dislike answers)
- Conversation history or multi-turn dialogues (each question is independent)
- Custom chunking strategies or user-defined chunk sizes
- A/B testing different models or retrieval strategies

## Dependencies

- Cohere API for embeddings (embed-english-v3.0) and answer generation (Command model)
- Qdrant Cloud for vector storage and similarity search
- Neon Serverless Postgres for metadata storage
- Textbook markdown content in a structured format (prerequisite for ingestion)
- Environment variables configured with API keys and database URLs

## Risks

- **Risk**: Cohere API rate limits or pricing changes could impact system availability
  - **Mitigation**: Monitor usage, implement caching for frequently asked questions, consider fallback models
- **Risk**: Chunking strategy may not preserve semantic meaning for all textbook sections (e.g., code examples split across chunks)
  - **Mitigation**: Test chunking on representative textbook sections, adjust strategy based on results
- **Risk**: Vector similarity search may not always retrieve the most relevant chunks (semantic gaps)
  - **Mitigation**: Evaluate retrieval quality with sample questions, tune similarity threshold, consider hybrid search (vector + keyword)
- **Risk**: Grounding mechanism may not prevent all hallucinations if the model generates content not in retrieved chunks
  - **Mitigation**: Implement strict prompting to limit generation to retrieved context, add post-generation validation

## Constitution Check

This specification adheres to the following constitution principles:

- **Spec-Driven Development (I)**: This specification defines all requirements before any implementation code is written
- **Clear Separation of Concerns (II)**: Backend is defined as a pure REST API with no frontend logic
- **Source-Grounded Answers Only (III)**: FR-013 explicitly requires no hallucinations, and SC-003/SC-004 measure grounding accuracy
- **Beginner-Friendly Explanations (IV)**: Answers are designed to support learners without advanced knowledge (though implementation will enforce this in prompting)
- **Production-Ready, Scalable Architecture (V)**: Stateless API design (FR-017), rate limiting (FR-014), environment-based config (FR-016)
- **Technology Stack Adherence**: Cohere for embeddings/generation, Qdrant for vectors, Neon for metadata as required by constitution
- **Required Environment Variables**: FR-016 mandates environment-variable-only configuration as per constitution constraints

---

**Next Steps**: Proceed to `/sp.plan` for implementation planning or `/sp.clarify` if additional clarification is needed.