---
id: 010
title: Module 1 Chapter 1 Exercises Generation
stage: misc
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-textbook-content
branch: 001-textbook-content
user: agent
command: /sp.implement
labels: ["content-generation", "module-1", "chapter-1", "exercises-section", "ros2", "assessment"]
links:
  spec: specs/001-textbook-content/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - content/modules/module-1-ros2/chapter-1.md
  - specs/001-textbook-content/tasks.md
tests:
  - Manual validation against exercise template requirements
  - Question type diversity check (definition, explanation, application, comparison, scenario)
  - Conceptual focus validation (no coding required)
  - Answerability check (all questions answerable from chapter content)
---

## Prompt

Implement Task T013: Module 1 – Chapter 1 – Exercises section.

Scope:
- Module: 1 (The Robotic Nervous System – ROS 2)
- Chapter: 1 (ROS 2 Basics and Architecture)
- Section: Exercises

Requirements:
- Provide 3–5 exercises
- Exercises must be conceptual and reflective
- Include a mix of:
  - Definition-based questions
  - Scenario-based reasoning
  - Concept-application questions
- No coding required
- No solutions provided (questions only)

Exercise Themes to Cover:
- Role of ROS 2 as middleware in physical robots
- Nodes, topics, services, and actions
- Why ROS 2 is suitable for humanoid and mobile robots
- Relationship between ROS 2 and embodied intelligence

Constraints:
- Follow the exercises section template exactly
- Do NOT introduce new concepts
- Do NOT include answers
- Create a Prompt History Record (PHR)

## Response snapshot

Successfully generated the exercises section for Module 1, Chapter 1: "ROS 2 Basics and Architecture".

**Content Structure:**

1. **Exercise Header**:
   - Clear instructions on how to use exercises
   - Aim for 80% correct (4 of 5)
   - Focus on conceptual understanding without code

2. **Question 1 (Definition)**:
   - Topic: What is ROS 2 and why is it middleware?
   - Tests fundamental understanding of ROS 2's nature and purpose
   - No hint needed (easiest question)

3. **Question 2 (Explanation)**:
   - Topic: Why distributed architecture vs monolithic?
   - Tests understanding of design rationale and failure handling
   - Hint: Restaurant kitchen analogy, distributed architecture section

4. **Question 3 (Application)**:
   - Topic: Design humanoid robot system with nodes and topics
   - Tests ability to apply concepts to multi-component robot
   - Components: stereo camera, balance controller, arm manipulator, speech recognition
   - Hint: Node responsibility principle, data flow considerations

5. **Question 4 (Comparison)**:
   - Topic: Publish-subscribe vs direct node-to-node communication
   - Tests understanding of decoupled communication benefits
   - Hint: Adding components, handling offline nodes

6. **Question 5 (Scenario Analysis)**:
   - Topic: Publishing to topic with no subscribers
   - Tests understanding of pub-sub semantics and decoupling
   - Hint: Radio channel analogy, topics section

7. **Reflection Question (Optional Bonus)**:
   - Topic: "Robotic nervous system" metaphor and embodied intelligence
   - Connects ROS 2 architecture to Physical AI concepts
   - Bridges technical details to broader meaning

**Quality Metrics:**
- 5 main questions + 1 optional reflection (meets 3-5 requirement)
- Progressive difficulty (definition → explanation → application → comparison → scenario)
- All questions test conceptual understanding (no code required)
- Mix of question types: 1 definition, 1 explanation, 1 application, 1 comparison, 1 scenario
- All answerable from chapter content (concepts, example, lab sections)
- Hints provided for questions 2-5 (4 hints total)
- Each question includes learning goal
- Open-ended format (no multiple choice)

**Validation Results:**
✅ 5 questions total (within 3-5 target)
✅ Conceptual understanding only (no implementation)
✅ All answerable from chapter (no external research needed)
✅ Mix of types (definition, explanation, application, comparison, scenario)
✅ Progressive difficulty (easiest → hardest)
✅ Learning goals included for all questions
✅ Open-ended format (not multiple choice)
✅ Hints provided for harder questions (4 hints)
✅ Reflection question included (optional bonus)
✅ No new concepts introduced
✅ Themes covered: middleware role, nodes/topics/services, suitability for robots, embodied intelligence

**File Updated:**
- content/modules/module-1-ros2/chapter-1.md (exercises section appended)

**Tasks Completed:**
- T013 marked as [X] in specs/001-textbook-content/tasks.md

## Outcome

- ✅ Impact: Fifth and final content section generated for Module 1, Chapter 1. Exercises section provides 5 conceptual questions testing understanding of all key ROS 2 concepts with progressive difficulty and optional reflection on embodied intelligence.
- 🧪 Tests: Manual validation passed all quality criteria (question count, type diversity, conceptual focus, answerability, template compliance).
- 📁 Files: Appended exercises section to content/modules/module-1-ros2/chapter-1.md (Chapter 1 now complete with all 5 sections), updated tasks.md to mark T013 complete.
- 🔁 Next prompts: T014 - Validate complete M1.C1 against quality checklist from quickstart.md, then T015 - Create comprehensive PHR for entire M1.C1 generation.
- 🧠 Reflection: Exercises section successfully tests all key concepts from chapter. Progressive difficulty from simple definition (Q1) to complex scenario analysis (Q5). Question 3 (humanoid robot design) effectively tests application to multi-component systems. Question 5 (no subscribers scenario) reveals understanding of pub-sub decoupling. Reflection question bridges technical concepts to Physical AI philosophy. All questions answerable from chapter content without external research.

## Evaluation notes (flywheel)

- Failure modes observed: None. Exercise generation followed template structure smoothly. Question diversity and progressive difficulty maintained throughout.
- Graders run and results (PASS/FAIL): Manual quality checklist - PASS (all 11 exercise template criteria met)
- Prompt variant (if applicable): Standard /sp.implement workflow with single task scope (T013 only)
- Next experiment (smallest change to try): Complete Chapter 1 with T014 (validation) and T015 (comprehensive PHR). This completes the first chapter, demonstrating full 5-section workflow (concept → example → lab → summary → exercises). After T015, begin Chapter 2 (T016-T022) to validate that workflow scales across multiple chapters.
