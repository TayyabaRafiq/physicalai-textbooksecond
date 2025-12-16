# Implementation Plan: AI-Native Physical AI & Humanoid Robotics Textbook

**Branch**: `001-textbook-content` | **Date**: 2025-12-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-textbook-content/spec.md`

**Note**: This plan focuses on content generation workflow, not software implementation. The textbook content will be generated using Claude Code following Spec-Kit Plus methodology.

## Summary

Generate a comprehensive AI-native textbook covering Physical AI & Humanoid Robotics with 4 modules (12 chapters total). Each chapter includes concept explanation, example, hands-on lab, summary, and exercises. Content generation will follow a module-by-module, chapter-by-chapter workflow with review and validation at each stage. The textbook targets beginner learners with no prior robotics background, using simulation-first approach and beginner-friendly language.

## Technical Context

**Content Format**: Markdown (.md files) for Docusaurus
**Primary Dependencies**: Claude Code (content generation), Spec-Kit Plus (workflow), Docusaurus (future platform)
**Storage**: File-based (Markdown files in repository)
**Content Validation**: Manual review + automated checklist validation
**Target Platform**: Static site (Docusaurus on GitHub Pages)
**Project Type**: Documentation/content project
**Content Goals**: 12 chapters, each readable in 20-30 minutes with 30-60 minute labs
**Constraints**: Beginner-friendly language, no deep mathematics, simulation-first approach
**Scale/Scope**: 4 modules × 3 chapters = 12 chapters total, ~200-300 pages estimated

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Specification-Driven Development
- ✅ **COMPLIANT**: Complete specification exists at `specs/001-textbook-content/spec.md`
- ✅ **COMPLIANT**: All content will be generated from specifications (module/chapter specs to be created in Phase 1)
- ✅ **COMPLIANT**: Specification defines all 4 modules and chapter requirements

### Principle II: AI-Native Authoring
- ✅ **COMPLIANT**: Claude Code is the primary content author
- ✅ **COMPLIANT**: Spec-Kit Plus workflow manages content generation process
- ✅ **COMPLIANT**: PHRs will be created for all content generation sessions
- ✅ **COMPLIANT**: Module and chapter specifications will guide AI content generation

### Principle V: Beginner-Friendly Accessibility
- ✅ **COMPLIANT**: FR-005 mandates beginner-friendly language
- ✅ **COMPLIANT**: FR-006 prohibits deep mathematical derivations
- ✅ **COMPLIANT**: FR-021 requires technical terms defined on first use
- ✅ **COMPLIANT**: Success criteria SC-002 targets 90% term clarity for beginners

### Content Boundaries Alignment
- ✅ **COMPLIANT**: Scope limited to content generation only (FR-008)
- ✅ **COMPLIANT**: Explicitly excludes authentication, chatbot, personalization, translation per spec Out of Scope section

**Gate Status**: ✅ **PASSED** - All applicable constitution principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-content/
├── plan.md                    # This file (/sp.plan command output)
├── spec.md                    # Feature specification (complete)
├── research.md                # Phase 0: Content research and source identification
├── content-model.md           # Phase 1: Content structure and templates (replaces data-model.md)
├── module-outlines/           # Phase 1: Detailed outlines for each module
│   ├── module-1-ros2.md
│   ├── module-2-simulation.md
│   ├── module-3-isaac.md
│   └── module-4-vla.md
├── chapter-templates/         # Phase 1: Templates for chapter generation
│   ├── concept-template.md
│   ├── example-template.md
│   ├── lab-template.md
│   ├── summary-template.md
│   └── exercise-template.md
├── quickstart.md              # Phase 1: Content generation quickstart guide
└── tasks.md                   # Phase 2: Task breakdown (/sp.tasks command - NOT created by /sp.plan)
```

### Content Files (repository root)

```text
content/
├── modules/
│   ├── module-1-ros2/
│   │   ├── chapter-1.md
│   │   ├── chapter-2.md
│   │   └── chapter-3.md
│   ├── module-2-simulation/
│   │   ├── chapter-1.md
│   │   ├── chapter-2.md
│   │   └── chapter-3.md
│   ├── module-3-isaac/
│   │   ├── chapter-1.md
│   │   ├── chapter-2.md
│   │   └── chapter-3.md
│   └── module-4-vla/
│       ├── chapter-1.md
│       ├── chapter-2.md
│       └── chapter-3.md
├── labs/
│   ├── module-1/
│   ├── module-2/
│   ├── module-3/
│   └── module-4/
└── exercises/
    ├── module-1/
    ├── module-2/
    ├── module-3/
    └── module-4/
```

**Structure Decision**: Content-focused project structure with separate directories for modules, labs, and exercises. Markdown files will be generated using Claude Code and later integrated into Docusaurus. Content directory structure mirrors the 4-module, 3-chapter-per-module organization defined in spec.

## Complexity Tracking

*No constitution violations - this section intentionally empty.*

## Phase 0: Content Research & Source Identification

**Objective**: Identify authoritative sources, best practices, and content patterns for each module to ensure technical accuracy and beginner-friendly presentation.

### Research Tasks

1. **Module 1 - ROS 2 Research**
   - Task: Research beginner-friendly ROS 2 learning resources and tutorials
   - Focus: Identify best practices for explaining nodes, topics, messages, and services to beginners
   - Deliverable: List of authoritative ROS 2 sources (official docs, tutorials, beginner guides)

2. **Module 2 - Simulation Research**
   - Task: Research digital twin concepts and Gazebo/Unity simulation tutorials
   - Focus: Identify best practices for teaching simulation concepts without hardware requirements
   - Deliverable: List of authoritative simulation sources and beginner-friendly examples

3. **Module 3 - NVIDIA Isaac Research**
   - Task: Research NVIDIA Isaac documentation and AI robotics perception/planning resources
   - Focus: Identify beginner-accessible Isaac Sim examples and AI robotics concepts
   - Deliverable: List of Isaac platform sources and AI robotics learning materials

4. **Module 4 - VLA Systems Research**
   - Task: Research Vision-Language-Action systems, transformer models for robotics
   - Focus: Identify accessible explanations of multimodal AI for physical systems
   - Deliverable: List of VLA research papers, blog posts, and educational resources

5. **Beginner Pedagogy Research**
   - Task: Research best practices for technical writing aimed at beginners
   - Focus: Writing style guides, term definition patterns, example structures
   - Deliverable: Pedagogy guidelines for beginner-friendly technical content

6. **Hands-on Lab Patterns**
   - Task: Research effective simulation-based lab structures for online learning
   - Focus: 30-60 minute lab formats, free simulation tool usage, step-by-step instructions
   - Deliverable: Lab template structure and best practices

### Research Consolidation (research.md)

All research findings will be consolidated into `specs/001-textbook-content/research.md` with:
- **Authoritative Sources**: Primary references for each module
- **Content Patterns**: Proven approaches for beginner technical content
- **Lab Formats**: Effective hands-on lab structures
- **Writing Guidelines**: Style guide for beginner-friendly language

**Output**: `research.md` with all authoritative sources and content approach decisions documented

## Phase 1: Content Structure & Module Design

**Prerequisites**: `research.md` complete with authoritative sources identified

### Deliverable 1: Content Model (content-model.md)

Document the structure and relationships of content entities:

**Content Entities**:
- **Module**: Title, learning objectives, prerequisites, 3 chapters
- **Chapter**: Title, learning goals, 5 sections (concept, example, lab, summary, exercises)
- **Concept Section**: Main explanation text, technical terms with definitions, diagrams/illustrations
- **Example Section**: Practical scenario demonstrating concept application
- **Lab Section**: Step-by-step hands-on activity, setup instructions, expected outcomes
- **Summary Section**: Key takeaways, concept recap
- **Exercise Section**: 3-5 conceptual questions testing understanding

**Content Validation Rules** (from spec):
- Each chapter must include all 5 sections (FR-003)
- Technical terms must be defined on first use (FR-021)
- Summaries must recap key concepts (FR-022)
- Exercises must test conceptual understanding only (FR-023)

**Content Relationships**:
- Modules are sequential with dependencies (M1→M2→M3→M4)
- Chapters within a module build progressively
- Labs reference concepts from same chapter
- Exercises test concepts from same chapter

### Deliverable 2: Module Outlines (module-outlines/)

Create detailed outlines for each module specifying exact chapter titles and learning objectives:

**module-1-ros2.md** (Module 1: The Robotic Nervous System):
- Chapter 1: ROS 2 Basics and Architecture
- Chapter 2: Nodes, Topics, and Message Passing
- Chapter 3: ROS 2 Simulation with Gazebo

**module-2-simulation.md** (Module 2: Digital Twin & Simulation):
- Chapter 1: Digital Twin Concepts for Physical AI
- Chapter 2: Gazebo Simulation Fundamentals
- Chapter 3: Unity for Robot Simulation

**module-3-isaac.md** (Module 3: AI Robot Brain):
- Chapter 1: AI-Driven Robot Intelligence Overview
- Chapter 2: NVIDIA Isaac Sim and Perception
- Chapter 3: Planning and Control with Isaac

**module-4-vla.md** (Module 4: Vision-Language-Action Systems):
- Chapter 1: Multimodal AI for Robotics
- Chapter 2: Vision-Language-Action Model Architectures
- Chapter 3: VLA Systems in Humanoid Robots

Each outline includes:
- Module learning objectives
- Chapter titles and learning goals
- Key concepts to cover
- Lab activity descriptions
- Prerequisite knowledge

### Deliverable 3: Chapter Templates (chapter-templates/)

Create templates for consistent chapter generation:

**concept-template.md**: Structure for concept explanations
- Introduction paragraph
- Key concept definitions (with beginner-friendly analogies)
- Technical term definitions
- Diagram/illustration placeholders
- Transition to example

**example-template.md**: Structure for practical examples
- Scenario setup
- Step-by-step walkthrough
- Expected outcomes
- Connection to real-world applications

**lab-template.md**: Structure for hands-on labs
- Lab objectives
- Prerequisites and setup
- Step-by-step instructions
- Checkpoints and expected results
- Troubleshooting tips
- Estimated time: 30-60 minutes

**summary-template.md**: Structure for chapter summaries
- Key concepts recap (3-5 bullet points)
- Important terms review
- Transition to next chapter

**exercise-template.md**: Structure for exercises
- 3-5 conceptual questions
- Question types: definition, explanation, application, comparison
- Focus on understanding, not implementation

### Deliverable 4: Quickstart Guide (quickstart.md)

Document the content generation workflow:

**Workflow Steps**:
1. Select module and chapter from module outline
2. Use chapter templates to structure content
3. Generate content section-by-section (concept → example → lab → summary → exercises)
4. Validate against quality checklist (beginner-friendly, terms defined, no deep math)
5. Review and refine
6. Create PHR for generation session
7. Move to next chapter

**Quality Checklist** (per chapter):
- [ ] All technical terms defined on first use
- [ ] Language accessible to beginners (no assumed robotics knowledge)
- [ ] No deep mathematical derivations
- [ ] Example is practical and clear
- [ ] Lab uses free simulation tools
- [ ] Lab completable in 30-60 minutes
- [ ] Summary recaps key concepts
- [ ] Exercises test conceptual understanding only

**Content Generation Order**: Module 1 → Module 2 → Module 3 → Module 4 (sequential)

### Phase 1 Summary

**Outputs**:
- `content-model.md`: Content entity structure and validation rules
- `module-outlines/`: 4 detailed module outlines with chapter specifications
- `chapter-templates/`: 5 templates for consistent chapter generation
- `quickstart.md`: Content generation workflow and quality checklist

**Readiness Gate**: After Phase 1, all content structure is defined and ready for chapter-by-chapter generation in implementation phase.

## Re-Evaluation: Constitution Check (Post-Phase 1)

### Principle I: Specification-Driven Development
- ✅ **COMPLIANT**: Module outlines serve as chapter-level specifications
- ✅ **COMPLIANT**: Chapter templates ensure consistent structure per spec requirements
- ✅ **COMPLIANT**: Content model documents all entities and validation rules

### Principle II: AI-Native Authoring
- ✅ **COMPLIANT**: Templates structured for AI content generation
- ✅ **COMPLIANT**: Quickstart guide defines Claude Code generation workflow
- ✅ **COMPLIANT**: PHR creation integrated into content generation process

### Principle V: Beginner-Friendly Accessibility
- ✅ **COMPLIANT**: Quality checklist enforces beginner-friendly language
- ✅ **COMPLIANT**: Templates include term definition requirements
- ✅ **COMPLIANT**: Example and lab templates emphasize accessibility

**Final Gate Status**: ✅ **PASSED** - All principles satisfied post-design

## Next Steps

This plan completes with Phase 1 design artifacts. Next command:

**`/sp.tasks`**: Generate task breakdown for content generation
- Tasks will be organized by module and chapter
- Each chapter generation will be a discrete task
- Review and validation tasks will be included
- PHR creation tasks for each content generation session

## Architectural Decisions

📋 **Architectural decision detected**: Content-first vs. Platform-first approach — This plan prioritizes content generation before Docusaurus integration. Document reasoning and trade-offs? Run `/sp.adr content-generation-approach`

📋 **Architectural decision detected**: Module-by-module sequential vs. parallel generation — This plan uses sequential module generation (M1→M2→M3→M4) rather than parallel. Document reasoning? Run `/sp.adr sequential-module-generation`