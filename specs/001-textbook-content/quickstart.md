# Content Generation Quickstart Guide

**Feature**: 001-textbook-content
**Purpose**: Step-by-step workflow for generating textbook chapters using Claude Code
**Prerequisites**: All Phase 1 artifacts complete (research.md, content-model.md, module outlines, chapter templates)

---

## Overview

This guide provides the recommended workflow for generating high-quality textbook content chapter-by-chapter using Claude Code and the templates/research created in Phase 1.

**Content Generation Approach**:
- **Sequential by Module**: Generate Module 1 → Module 2 → Module 3 → Module 4
- **Chapter-by-Chapter**: Complete one full chapter before starting the next
- **Section-by-Section**: Within each chapter, generate concept → example → lab → summary → exercises
- **Review and Validate**: After each chapter, run quality checklist before proceeding

---

## Content Generation Workflow

### Step 1: Select Module and Chapter

**Decision Point**: What to generate next?

**Recommended Order**:
1. Module 1, Chapter 1: ROS 2 Basics and Architecture
2. Module 1, Chapter 2: Nodes, Topics, and Message Passing
3. Module 1, Chapter 3: ROS 2 Simulation with Gazebo
4. Module 2, Chapter 1: Digital Twin Concepts for Physical AI
5. Module 2, Chapter 2: Gazebo Simulation Fundamentals
6. Module 2, Chapter 3: Unity for Robot Simulation
7. Module 3, Chapter 1: AI-Driven Robot Intelligence Overview
8. Module 3, Chapter 2: NVIDIA Isaac Sim and Perception
9. Module 3, Chapter 3: Planning and Control with Isaac
10. Module 4, Chapter 1: Multimodal AI for Robotics
11. Module 4, Chapter 2: Vision-Language-Action Model Architectures
12. Module 4, Chapter 3: VLA Systems in Humanoid Robots

**Resources to Reference**:
- **Module Outline**: `specs/001-textbook-content/module-outlines/module-[N]-[name].md`
- **Research**: `specs/001-textbook-content/research.md` (authoritative sources for this module)
- **Content Model**: `specs/001-textbook-content/content-model.md` (structure and validation rules)

---

### Step 2: Prepare Chapter Context

Before generating content, gather these resources:

**For [Module N, Chapter M]**:

1. **Read Module Outline**:
   - File: `specs/001-textbook-content/module-outlines/module-[N]-[name].md`
   - Note: Chapter title, learning goals, key concepts, lab description

2. **Review Research Findings**:
   - File: `specs/001-textbook-content/research.md`
   - Section: Module [N] - find authoritative sources and content patterns

3. **Check Prerequisite Chapters** (if not Chapter 1):
   - Ensure previous chapters in module are complete
   - Review what concepts have been introduced (to build upon vs. repeat)

4. **Load Chapter Templates**:
   - Concept: `specs/001-textbook-content/chapter-templates/concept-template.md`
   - Example: `specs/001-textbook-content/chapter-templates/example-template.md`
   - Lab: `specs/001-textbook-content/chapter-templates/lab-template.md`
   - Summary: `specs/001-textbook-content/chapter-templates/summary-template.md`
   - Exercise: `specs/001-textbook-content/chapter-templates/exercise-template.md`

---

### Step 3: Generate Chapter Sections (Sequential)

Generate each section in order, using the templates as structure:

#### 3a. Generate Concept Explanation Section

**Template**: `chapter-templates/concept-template.md`

**Inputs**:
- Key concepts from module outline for this chapter
- Authoritative sources from research.md
- Content patterns from research.md (analogies, pedagogical approaches)

**Process**:
1. Start with introduction (hook + context + preview)
2. For each key concept (3-5 total):
   - Define in plain English first
   - Provide technical definition
   - Give concrete example
   - Explain why it matters
3. Define all technical terms on first use
4. Mark diagram placeholders where visuals would help
5. End with transition to example section

**Quality Check**:
- [ ] All technical terms defined
- [ ] Language beginner-friendly (no assumed robotics knowledge)
- [ ] No deep mathematical derivations
- [ ] Analogies used where appropriate
- [ ] 800-1200 words total

**Output**: Save to `content/modules/module-[N]-[name]/chapter-[M]-concept.md` (temporary working file)

---

#### 3b. Generate Simple Example Section

**Template**: `chapter-templates/example-template.md`

**Inputs**:
- Example scenario from module outline
- Concepts just explained in 3a
- Real-world connection ideas from research.md

**Process**:
1. Set up scenario (context + problem)
2. Walk through 3-5 steps showing concepts in action
3. Describe expected outcomes
4. Connect to real-world applications

**Quality Check**:
- [ ] Example uses simulation (no physical hardware)
- [ ] Each step explicitly ties to a concept from section 3a
- [ ] Scenario is relatable and practical
- [ ] 400-600 words total

**Output**: Append to chapter file or save as `chapter-[M]-example.md`

---

#### 3c. Generate Hands-On Lab Section

**Template**: `chapter-templates/lab-template.md`

**Inputs**:
- Lab description from module outline
- Research findings for this module (lab patterns, tools, common pitfalls)
- Concepts from 3a that lab should reinforce

**Process**:
1. Write lab header (objectives, prerequisites, setup)
2. Create setup instructions with verification steps
3. Break lab into 2-4 parts, each with:
   - Clear goal
   - 3-7 actionable steps with expected outcomes
   - Checkpoint for verification
4. Add troubleshooting section (3-5 common issues)
5. Add optional extension activities
6. Write lab summary (accomplishments + takeaways)

**Quality Check**:
- [ ] Estimated time: 30-60 minutes
- [ ] Uses only free simulation tools
- [ ] Every step has expected outcome
- [ ] Checkpoints every 3-5 steps
- [ ] Troubleshooting addresses common errors
- [ ] Setup includes verification commands

**Output**: Append to chapter file or save as `chapter-[M]-lab.md`

---

#### 3d. Generate Summary Section

**Template**: `chapter-templates/summary-template.md`

**Inputs**:
- All concepts from section 3a
- Technical terms defined throughout chapter
- Next chapter preview from module outline

**Process**:
1. Recap 3-5 key concepts (restate in fresh language)
2. List all technical terms with one-sentence definitions
3. Show chapter's place in module progression
4. Preview next chapter (title + 3 bullet points + why it matters)
5. Add encouraging closing statement

**Quality Check**:
- [ ] Concepts restated (not copy-pasted)
- [ ] All technical terms listed
- [ ] Module progress indicated
- [ ] Next chapter previewed
- [ ] 200-300 words total

**Output**: Append to chapter file or save as `chapter-[M]-summary.md`

---

#### 3e. Generate Exercises Section

**Template**: `chapter-templates/exercise-template.md`

**Inputs**:
- Key concepts from section 3a
- Learning objectives from module outline

**Process**:
1. Write 3-5 questions in order:
   - Q1: Definition (easiest)
   - Q2: Explanation (why/how)
   - Q3: Application (scenario-based)
   - Q4: Comparison (tradeoffs)
   - Q5: Analysis (complex scenario) - optional
2. For each question:
   - State learning goal
   - Add hint if needed
3. Add optional reflection question

**Quality Check**:
- [ ] 3-5 questions total
- [ ] All answerable from chapter content
- [ ] No implementation/coding questions
- [ ] Mix of question types
- [ ] Progressive difficulty
- [ ] Learning goals stated

**Output**: Append to chapter file or save as `chapter-[M]-exercises.md`

---

### Step 4: Assemble Complete Chapter

Combine all sections into a single chapter file:

**File Structure**:
```markdown
# Module [N], Chapter [M]: [Chapter Title]

## Introduction
[Brief chapter overview - 1 paragraph]

---

## Concept Explanation
[Content from 3a]

---

## Example: [Example Title]
[Content from 3b]

---

## Hands-On Lab: [Lab Title]
[Content from 3c]

---

## Chapter Summary
[Content from 3d]

---

## Exercises
[Content from 3e]

---

**End of Chapter [M]**
```

**Output File**: `content/modules/module-[N]-[name]/chapter-[M].md`

---

### Step 5: Validate Chapter Quality

Run the chapter through this quality checklist:

#### Content Quality

- [ ] All technical terms defined on first use
- [ ] Analogies used to explain unfamiliar concepts
- [ ] Concrete examples before abstract explanations
- [ ] Diagram placeholders marked for spatial/process concepts
- [ ] No assumed prior robotics knowledge

#### Beginner-Friendly Language

- [ ] Average sentence length ≤ 20 words
- [ ] Active voice used (>80% of sentences)
- [ ] Jargon avoided or immediately defined
- [ ] Second person ("you") used for direct address
- [ ] Encouraging, not intimidating tone

#### Structure and Flow

- [ ] Chapter follows 5-section structure (concept → example → lab → summary → exercises)
- [ ] Prerequisites stated (if any beyond previous chapters)
- [ ] Transitions between sections are smooth
- [ ] Summary recaps all key concepts
- [ ] Exercises test conceptual understanding only

#### Lab Quality

- [ ] Objectives clear and measurable
- [ ] Estimated time realistic (30-60 min)
- [ ] Setup instructions complete with verification
- [ ] Each step includes expected outcome
- [ ] Checkpoints every 3-5 steps
- [ ] Troubleshooting addresses common errors
- [ ] Only free simulation tools used
- [ ] Optional extensions for advanced learners

#### Spec Compliance

- [ ] Content aligns with FR requirements from spec.md
- [ ] Authoritative sources cited where applicable
- [ ] Examples realistic and relevant
- [ ] No deep mathematical derivations (FR-006)
- [ ] Simulation-first approach maintained (FR-007)
- [ ] Beginner-friendly language (FR-005)

**If any items fail**: Revise chapter before proceeding

---

### Step 6: Create Prompt History Record (PHR)

After completing a chapter, create a PHR to document the generation session:

**PHR Details**:
- **Stage**: "misc" (content generation is a miscellaneous implementation task)
- **Title**: "[Module N Chapter M] Content Generation"
- **Feature**: "001-textbook-content"
- **Files**: List the chapter file created
- **Prompt**: Record the inputs used (module outline, research, templates)
- **Response**: Summarize what was generated and key decisions made

**Location**: `history/prompts/001-textbook-content/[ID]-module-[N]-chapter-[M]-generation.misc.prompt.md`

---

### Step 7: Move to Next Chapter

**Decision Point**: Is the current module complete?

**If current module incomplete** (not all 3 chapters done):
- Return to Step 1, select next chapter in same module
- Review previous chapter to understand what's been established

**If current module complete** (all 3 chapters done):
- Review entire module for consistency
- Return to Step 1, select Chapter 1 of next module

**If all 4 modules complete** (12 chapters total):
- Proceed to textbook-wide validation and finalization
- Create table of contents, introduction, conclusion
- Add glossary of all technical terms
- Prepare for Docusaurus integration (separate feature)

---

## Quality Standards Reference

### Per-Chapter Targets (from spec.md and content-model.md)

| Metric | Target | Source |
|--------|--------|--------|
| **Chapter Reading Time** | 20-30 minutes | Assumption 4 in spec.md |
| **Lab Duration** | 30-60 minutes | FR-003, SC-003, Assumption 1 |
| **Exercise Success Rate** | 80% correct | SC-004, Assumption 2 |
| **Technical Term Clarity** | 90% understandable to beginners | SC-002 |
| **Concept Section Length** | 800-1200 words | Content model |
| **Example Section Length** | 400-600 words | Content model |
| **Summary Section Length** | 200-300 words | Content model |
| **Exercise Count** | 3-5 questions | Content model |

### Content Validation Rules (from content-model.md)

- Each chapter MUST include all 5 sections: concept, example, lab, summary, exercises (FR-003)
- Technical terms MUST be defined on first use (FR-021)
- Chapter summaries MUST recap key concepts (FR-022)
- Exercises MUST test conceptual understanding only (FR-023)
- Content MUST use beginner-friendly language (FR-005)
- Content MUST avoid deep mathematical derivations (FR-006)
- Examples MUST use simulation-first approach (FR-007)

---

## Troubleshooting Common Issues

### Issue: Running Out of Ideas for Examples

**Solution**:
- Review research.md for real-world applications
- Check module outline for suggested scenarios
- Look at authoritative sources (ROS 2 docs, Isaac examples) for inspiration
- Ask: "What problem does this concept solve in practice?"

---

### Issue: Lab Seems Too Complex for 30-60 Minutes

**Solution**:
- Break into smaller parts with clear checkpoints
- Simplify by using pre-built components (don't build from scratch)
- Focus on one key concept per lab (not everything at once)
- Test the lab yourself to verify time estimate

---

### Issue: Exercises Feel Too Easy/Hard

**Solution**:
- Mix question types (definition, explanation, application, comparison)
- Use progressive difficulty (easier → harder)
- Target 80% success rate (most learners should get 4 out of 5)
- If too hard: Add hints or simplify wording
- If too easy: Add application/analysis questions

---

### Issue: Chapter Doesn't Flow Well

**Solution**:
- Check transitions between sections
- Ensure example builds on concepts from concept section
- Verify lab reinforces what example demonstrated
- Confirm summary accurately recaps entire chapter
- Read aloud to catch awkward phrasing

---

### Issue: Unclear if Content is Beginner-Friendly

**Solution**:
- Read as if you know nothing about robotics
- Check for undefined jargon
- Verify analogies are to familiar concepts (not other technical topics)
- Use active voice and simple sentence structure
- Ask: "Could a motivated learner with basic programming knowledge understand this?"

---

## Tools and Resources Quick Reference

### Phase 1 Artifacts (Already Created)

| File | Purpose |
|------|---------|
| `research.md` | Authoritative sources, content patterns, lab structures |
| `content-model.md` | Entity structure, validation rules, quality standards |
| `module-outlines/module-[N]-[name].md` | Chapter titles, learning goals, key concepts, lab descriptions |
| `chapter-templates/*.md` | Templates for each of the 5 chapter sections |
| `plan.md` | Overall implementation plan and Phase 1 design |

### Output Directory Structure

```
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
```

### Authoritative Source Links (from research.md)

**ROS 2**: https://docs.ros.org/en/jazzy/
**Gazebo**: https://gazebosim.org/docs
**Unity Robotics**: https://github.com/Unity-Technologies/Unity-Robotics-Hub
**Isaac Sim**: https://docs.omniverse.nvidia.com/isaacsim/latest/
**RT-1/RT-2**: https://robotics-transformer.github.io/

---

## Example: Generating Module 1, Chapter 1

**Step 1**: Select Module 1, Chapter 1: "ROS 2 Basics and Architecture"

**Step 2**: Prepare Context
- Read: `module-outlines/module-1-ros2.md` → Chapter 1 section
- Review: `research.md` → Module 1 section
- Load: All 5 chapter templates

**Step 3**: Generate Sections

**3a. Concept Section**:
- Key concepts: ROS 2 as nervous system, distributed architecture, ROS graph, nodes, topics, DDS
- Use "nervous system" analogy from research.md
- Define: ROS 2, Node, Topic, DDS, ROS Graph
- Target: 1000 words

**3b. Example Section**:
- Scenario: Robot delivery system coordinating camera, navigation, wheels (from module outline)
- Show how ROS 2 enables independent components to work together
- Target: 500 words

**3c. Lab Section**:
- Lab: "Install ROS 2 and Explore the Environment" (from module outline)
- Duration: 45-60 minutes
- Parts: Install ROS 2 → Run demo nodes → Visualize graph → Explore topics
- Troubleshooting: Address "command not found" (sourcing issue)

**3d. Summary Section**:
- Recap: ROS 2 as nervous system, distributed architecture, graph visualization
- Terms: List all 5 technical terms with definitions
- Next chapter: Preview "Nodes, Topics, and Message Passing"
- Target: 250 words

**3e. Exercises**:
- Q1 (Definition): What is ROS 2?
- Q2 (Explanation): Why distributed architecture?
- Q3 (Application): Design nodes for a specific robot
- Q4 (Comparison): Distributed vs. centralized control
- 4 questions total

**Step 4**: Assemble into `content/modules/module-1-ros2/chapter-1.md`

**Step 5**: Validate against quality checklist (all items pass)

**Step 6**: Create PHR documenting generation session

**Step 7**: Move to Module 1, Chapter 2

---

## Summary

This quickstart guide provides the step-by-step workflow for generating all 12 chapters of the AI-Native Physical AI & Humanoid Robotics textbook. By following this process—selecting chapters sequentially, using templates for structure, referencing research for content, and validating quality at each step—you ensure consistent, high-quality, beginner-friendly educational content that meets all specification requirements.

**Next Command**: `/sp.tasks` to generate the task breakdown for content generation based on this workflow.