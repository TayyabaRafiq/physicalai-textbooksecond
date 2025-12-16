# Simple Example Template

**Purpose**: Structure for generating practical example sections
**Target Length**: 400-600 words
**Validation**: Simulation-first, practical, connects to real-world

---

## Template Structure

### 1. Scenario Setup

**Purpose**: Establish context and problem for the example

**Content**:
- **Scenario Title**: Descriptive name (e.g., "Warehouse Package Sorting Robot")
- **Context**: What the robot needs to accomplish
- **Problem**: Challenge that requires the concepts from this chapter
- **Why This Scenario**: Connection to real-world applications

**Example**:

#### Scenario: [Descriptive Title]

Imagine [context setting - describe the environment and situation]. The robot's task is to [specific goal], but it faces a challenge: [problem that concepts from this chapter solve].

This scenario represents real-world applications in [domain, e.g., warehouse automation, autonomous vehicles, healthcare robotics], where [broader significance].

---

### 2. Step-by-Step Walkthrough

**Purpose**: Demonstrate how concepts apply to solve the problem

**Content**:
- **Step format**: Numbered or bulleted steps
- **Each step**: What happens + which concept it demonstrates
- **Data flow**: Show how information moves through the system (if applicable)
- **Visual cues**: Note where diagrams would help

**Structure**:

**How the Robot Solves This Challenge:**

1. **[Step Name]**: [What the robot does]
   - **Concept Applied**: [Which concept from earlier section]
   - **In Action**: [Specific details of how concept works here]

2. **[Step Name]**: [Next action]
   - **Concept Applied**: [Relevant concept]
   - **In Action**: [Specific application]

3. **[Step Name]**: [Further action]
   - **Concept Applied**: [Relevant concept]
   - **In Action**: [Specific application]

[Continue for 3-5 steps total]

**Example**:

**How the Delivery Robot Navigates:**

1. **Perceive the Environment**
   - **Concept Applied**: Sensor data processing (from concept section)
   - **In Action**: The robot's lidar scans the hallway, detecting walls at 2 meters left/right and a person 5 meters ahead

2. **Plan a Safe Path**
   - **Concept Applied**: Path planning algorithms
   - **In Action**: Using the lidar data, the robot calculates a trajectory that maintains 1.5-meter clearance from the person

3. **Execute Movement**
   - **Concept Applied**: Control commands via topics
   - **In Action**: The robot sends velocity commands to its motors, following the planned path while continuously updating based on new sensor data

---

### 3. Expected Outcomes

**Purpose**: Show results of applying the concepts

**Content**:
- **What happens**: Observable outcome of the scenario
- **Success criteria**: How to tell the concepts worked
- **Failures without concepts**: Contrast with naive approach

**Example**:

**What Happens:**

The robot successfully [outcome of scenario]. Key indicators of success include:
- [Observable result 1, e.g., "The robot maintains safe distance from obstacles"]
- [Observable result 2, e.g., "Navigation completes in 30 seconds"]
- [Observable result 3, e.g., "No collisions occur despite dynamic environment"]

Without the concepts covered in this chapter, the robot would [failure mode, e.g., "collide with obstacles due to poor perception"] or [limitation, e.g., "navigate too slowly due to inefficient planning"].

---

### 4. Real-World Connection

**Purpose**: Connect example to broader Physical AI applications

**Content**:
- **Industry applications**: Where this is used today
- **Variations**: How the same concepts apply in different contexts
- **Future potential**: Where this technology is heading

**Example**:

**Real-World Applications:**

This navigation example reflects challenges in:
- **[Industry 1]**: [How concepts apply, e.g., "Warehouse robots navigating aisles to retrieve inventory"]
- **[Industry 2]**: [How concepts apply, e.g., "Autonomous vehicles planning lane changes"]
- **[Industry 3]**: [How concepts apply, e.g., "Surgical robots positioning instruments precisely"]

The same fundamental concepts—[concept 1], [concept 2], and [concept 3]—enable all these applications, demonstrating the broad importance of Physical AI perception and planning.

---

## Quality Checklist (Use When Generating)

- [ ] Scenario is relatable and practical
- [ ] Problem clearly requires concepts from chapter
- [ ] Walkthrough has 3-5 clear steps
- [ ] Each step explicitly connects to a concept
- [ ] Expected outcomes are observable and specific
- [ ] Real-world connections span multiple applications
- [ ] No physical hardware required (simulation-first)
- [ ] Example is understandable to beginners
- [ ] Total length: 400-600 words

---

## Example Scenarios by Module

**Module 1 (ROS 2)**:
- Package delivery robot coordinating camera + navigation + wheels
- Multi-robot warehouse system communicating via topics
- Robotic arm with separate perception and control nodes

**Module 2 (Simulation)**:
- Testing navigation algorithms safely in Gazebo before physical deployment
- Training object recognition in photorealistic Unity simulation
- Parallel simulation runs to test edge cases

**Module 3 (Isaac AI)**:
- Object detection for warehouse picking using Isaac Sim
- RL-trained robot learning to navigate cluttered spaces
- Perception-planning-control loop for autonomous manipulation

**Module 4 (VLA)**:
- Household robot following natural language instructions
- Humanoid robot generalizing to novel objects via VLA
- Multi-step task execution from high-level language commands

---

## Anti-Patterns to Avoid

❌ **Don't**: Create overly complex scenarios with many moving parts
✅ **Do**: Keep scenarios focused on demonstrating 2-3 key concepts

❌ **Don't**: Use industry jargon without explanation
✅ **Do**: Explain domain-specific terms as they arise

❌ **Don't**: Make examples require physical hardware
✅ **Do**: Use simulation-based or conceptual examples

❌ **Don't**: Skip the "why this matters" connection
✅ **Do**: Always link back to real-world Physical AI applications

❌ **Don't**: Present example without tying to concepts
✅ **Do**: Explicitly label which concepts each step demonstrates