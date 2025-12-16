<!--
Sync Impact Report:
- Version: Initial (none) → 1.0.0
- Changes: Initial constitution creation for AI-native textbook project
- Added sections: All sections (initial creation)
- Templates status:
  ✅ .specify/templates/plan-template.md (reviewed - compatible)
  ✅ .specify/templates/spec-template.md (reviewed - compatible)
  ✅ .specify/templates/tasks-template.md (reviewed - compatible)
- Follow-up: None
- Date: 2025-12-15
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Specification-Driven Development

All content, features, and systems MUST originate from written specifications before implementation.

- Specifications are the single source of truth for the project
- No code or content is written without a corresponding spec in `specs/` directory
- Specifications MUST be reviewed and approved before implementation begins
- Changes to scope require specification updates first

**Rationale**: Spec-driven development ensures clarity, traceability, and AI-assisted generation consistency across the entire textbook and platform.

### II. AI-Native Authoring

The textbook MUST be authored using Claude Code as the primary co-author and development partner.

- All content generation leverages Claude Code and Spec-Kit Plus
- AI is treated as a co-author, not just a tool
- Prompts and AI interactions MUST be recorded in Prompt History Records (PHRs)
- Specifications guide AI-generated content to ensure quality and consistency

**Rationale**: AI-native authoring demonstrates the future of educational content creation and serves as a working example for the Panaversity ecosystem.

### III. Unified Project Architecture

The textbook, chatbot, and supporting systems MUST be part of one coherent, integrated project.

- Docusaurus serves as the unified platform for content delivery
- AI chatbot is embedded directly in the published book
- Backend APIs and RAG systems are integral components, not separate projects
- All components share common specifications and documentation

**Rationale**: A unified architecture prevents fragmentation, reduces complexity, and demonstrates real-world AI system integration.

### IV. Interactive Learning

The published textbook MUST provide interactive, AI-assisted learning capabilities.

- Embedded AI chatbot answers questions using RAG on full book content
- Users MUST be able to select text and ask context-specific questions
- Learning interactions are adaptive and contextual
- Chatbot responses cite specific book sections and provide accurate information

**Rationale**: Interactive learning transforms passive reading into active engagement, demonstrating the power of AI-assisted education.

### V. Beginner-Friendly Accessibility

Content MUST be accessible to learners without prior robotics or advanced AI knowledge.

- Explanations prioritize clarity over mathematical rigor
- Complex concepts are introduced progressively with practical examples
- Technical jargon is defined and explained on first use
- Content balances conceptual understanding with practical application

**Rationale**: As part of the Panaversity mission, the textbook must welcome learners from diverse backgrounds into Physical AI and robotics.

### VI. Technology Stack Adherence

Implementation MUST use the specified technology stack without deviation.

**Book Platform**: Docusaurus (for content publishing and GitHub Pages deployment)
**AI Authoring**: Claude Code (primary development environment)
**Specification System**: Spec-Kit Plus (for spec-driven workflows)
**Backend APIs**: FastAPI (for chatbot and RAG endpoints)
**AI Interaction**: OpenAI Agents / ChatKit SDKs (for chatbot intelligence)
**Data Storage**: Neon Serverless Postgres (for persistent data)
**Vector Search**: Qdrant Cloud Free Tier (for RAG embeddings)

**Rationale**: Standardized technology choices ensure maintainability, free/low-cost deployment, and alignment with Panaversity infrastructure.

### VII. Deployment Readiness

The final system MUST be deployable to GitHub Pages as a complete, functional learning platform.

- All components (book + chatbot + APIs) MUST be deployment-ready
- Configuration for GitHub Pages MUST be included
- Free-tier services (Neon, Qdrant) MUST be configured and documented
- Deployment instructions MUST be clear and reproducible

**Rationale**: Deployment readiness ensures the project delivers a working system, not just documentation or prototypes.

## Success Criteria

The project achieves its goals when:

1. **Standalone Learning Resource**: The book can be read independently without external resources
2. **Accurate AI Assistance**: The chatbot correctly answers questions using book content via RAG
3. **Spec-Driven Demonstration**: The project clearly demonstrates spec-driven thinking and AI-native development
4. **Extensibility Foundation**: The system architecture supports future personalization, translation, and adaptive features

## Explicit Non-Goals

This project does NOT aim to:

- Provide deep mathematical derivations or proofs (beginner-friendly focus)
- Teach hardware assembly, electronics, or circuit design (software/AI focus)
- Replace formal university robotics degrees (educational supplement)
- Optimize for any single hardware vendor or platform (vendor-neutral)
- Implement advanced research-level algorithms (practical learning focus)

## Content Boundaries

The textbook bridges digital intelligence (AI agents, LLMs) and physical embodiment (robots in the real world).

**In Scope**:
- Physical AI fundamentals and concepts
- Humanoid robotics principles and architectures
- AI agent integration with physical systems
- Practical examples and case studies
- Conceptual understanding of perception, planning, and control

**Out of Scope**:
- Low-level hardware interfacing and electronics
- Mathematical proofs and theoretical derivations
- Vendor-specific product training
- Research paper reproductions
- Production deployment and scalability optimizations

## Development Workflow

### Specification Process

1. Feature or content requirements are documented in `specs/<feature>/spec.md`
2. Specifications include user stories, requirements, and success criteria
3. AI (Claude Code) assists in specification refinement and validation
4. Specifications are reviewed before implementation begins

### Implementation Process

1. Implementation plans are created in `specs/<feature>/plan.md`
2. Tasks are broken down in `specs/<feature>/tasks.md`
3. Implementation follows TDD principles where applicable
4. All significant changes are tracked via PHRs in `history/prompts/`

### Architectural Decisions

When architecturally significant decisions are made:
- The decision MUST be documented in `history/adr/`
- ADRs capture context, options considered, and rationale
- ADRs are suggested during planning, never auto-created
- Suggestion format: "📋 Architectural decision detected: [brief] — Document reasoning? Run `/sp.adr <title>`"

## Quality Standards

### Content Quality

- Technical accuracy is verified against authoritative sources
- Explanations are clear, concise, and beginner-friendly
- Examples are practical and directly relevant to concepts
- Code samples are tested and functional

### Code Quality

- Backend APIs follow FastAPI best practices
- Frontend components follow React and Docusaurus conventions
- Code is documented with clear comments where needed
- Error handling is comprehensive and user-friendly

### AI Interaction Quality

- RAG responses cite specific book sections accurately
- Chatbot handles edge cases gracefully (no context, unclear questions)
- Selected-text queries work reliably and provide relevant answers
- Response latency is acceptable for learning interactions

## Governance

### Constitution Authority

This constitution supersedes all other project practices and guidelines. When conflicts arise, constitution principles take precedence.

### Amendment Process

1. Proposed changes are documented with rationale
2. Changes are reviewed for impact on existing specifications and implementations
3. Dependent templates and documentation are updated to maintain consistency
4. Version is incremented according to semantic versioning rules
5. Sync Impact Report is generated and included in the constitution file

### Versioning Policy

- **MAJOR**: Backward-incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance

- All specifications MUST reference and comply with relevant principles
- Implementation plans MUST include "Constitution Check" sections
- Pull requests MUST verify compliance with applicable principles
- Violations MUST be justified and documented in complexity tracking tables

**Version**: 1.0.0 | **Ratified**: 2025-12-15 | **Last Amended**: 2025-12-15