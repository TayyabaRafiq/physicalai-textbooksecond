---
sidebar_position: 3
---

# Chapter 3: Services and Actions

**Estimated Reading Time**: 15 minutes

---

## Concept Explanation: Beyond Publish-Subscribe

### Introduction

In Chapter 2, you learned how ROS 2 nodes communicate through the publish-subscribe pattern: publishers broadcast data on topics, subscribers receive it, and nobody knows (or cares) who's on the other end. This pattern works brilliantly for continuous data streams—sensor readings arriving 30 times per second, motor commands updating constantly, camera images flowing nonstop. But what happens when a robot needs a specific answer to a specific question? Or when it needs to execute a long-running task and monitor progress?

Imagine a humanoid robot asked to "bring me a glass of water." Publishing "start navigation" on a topic doesn't tell the robot whether it successfully reached the kitchen. The publish-subscribe pattern can't provide confirmation, can't report progress ("I'm halfway there"), and can't handle failure gracefully ("obstacle blocking path"). This chapter introduces **services** and **actions**—the ROS 2 communication patterns that complement pub-sub for Physical AI systems requiring request-response interactions and goal-oriented behaviors.

---

### Key Concepts

#### Services: Request-Response for Robot Queries

**Service**: A synchronous request-response communication pattern where a client node asks a server node for specific information or action, waits for completion, and receives a response—like calling a function on another computer.

**In Plain English**: Think of a service like asking a librarian for a book. You walk up (send request), ask for a specific title (provide parameters), wait while they retrieve it (server processes), and receive the book or a "not available" message (get response). You don't leave until you get an answer. Similarly, a robot's navigation planner might call a "calculate_path" service, providing start and goal positions, waiting for computation, and receiving the planned route or an error if no path exists.

**Why It Matters**: Services enable robots to ask questions and get definitive answers. When a humanoid robot needs to know "Can I grasp this object?" or "What's the battery percentage?", it can't rely on pub-sub broadcasting—it needs a direct query with a guaranteed response. Services provide this synchronous, two-way communication. The client (requester) waits for the server (responder) to finish processing, ensuring the robot receives critical information before proceeding.

**Example**: A warehouse robot approaches a door and calls the "check_door_status" service. The door sensor node (server) receives the request, checks if the door is open or closed, and responds with the current state. The robot waits for this response (blocking) before deciding whether to proceed through the doorway or request the door to open. Without services, the robot would have to subscribe to a door status topic and hope a message arrives at the right moment—unreliable and inefficient.

---

#### Actions: Long-Running Goals with Feedback

**Action**: An asynchronous goal-oriented communication pattern where a client sends a goal to a server, which executes it over time while providing periodic feedback and a final result—perfect for tasks that take seconds or minutes to complete.

**In Plain English**: Think of an action like ordering food delivery. You place an order (send goal), the restaurant accepts it (goal accepted), you receive updates ("preparing your meal," "out for delivery"—periodic feedback), and finally get confirmation when delivered (final result). You can check progress anytime or even cancel if plans change. Similarly, a humanoid robot given the goal "navigate to the kitchen" sends an action request. The navigation system accepts, provides feedback every second ("30% complete," current position), and sends a final result ("arrived" or "failed: obstacle").

**Why It Matters**: Actions solve the problem of long-running robot behaviors. Navigation might take 2 minutes, object grasping might take 10 seconds, and whole-body manipulation might take 30 seconds—these tasks are too slow for services (which block until complete) and too complex for pub-sub (which doesn't track completion). Actions provide three critical capabilities: (1) **feedback** (monitor progress in real-time), (2) **preemption** (cancel goals mid-execution if circumstances change), and (3) **asynchronous execution** (client can do other work while action runs). This enables responsive, interruptible robot behaviors essential for Physical AI.

**Example**: A humanoid robot receives the command "pick up the red cup." It sends a grasping action to its manipulation controller with the goal "grasp object at position X,Y,Z." The controller accepts the goal and begins: moving the arm (feedback: "approaching object, 40% complete"), opening the gripper (feedback: "gripper positioned, 70% complete"), closing around the cup (feedback: "grasping, 90% complete"). If the robot's vision system suddenly detects the cup moving, it can cancel (preempt) the action before the gripper closes. Finally, the controller sends the result: "success: object grasped" with grip force measurement, or "failed: object slipped" if grasping failed. The robot uses this information to decide next steps.

---

### How Services and Actions Fit Physical AI Systems

Together, pub-sub, services, and actions form ROS 2's complete communication toolkit:

- **Publish-Subscribe (Topics)**: Continuous data streams (sensors, motor commands, state updates)—used constantly for real-time perception and control
- **Services**: On-demand queries requiring immediate answers (configuration checks, calculations, one-time requests)—used occasionally when definitive responses needed
- **Actions**: Goal-oriented tasks with progress tracking (navigation, manipulation, multi-step behaviors)—used for high-level robot behaviors

A humanoid robot making breakfast uses all three: it **subscribes** to camera topics for vision (pub-sub), **calls** a path planning service to check if the kitchen is reachable (service), and **sends** a "crack egg" action to its manipulation system while monitoring gripper force feedback (action). This combination enables the responsive, goal-driven intelligence that defines Physical AI systems.

---

**Word Count**: ~590 words

---

## Example: Humanoid Home Assistant Fetching a Drink

### Scenario: Integrated Communication Patterns

Imagine a humanoid home assistant robot helping an elderly person living independently. The person asks, "Could you bring me a glass of water from the kitchen?" This simple request requires the robot to coordinate perception, navigation, manipulation, and safety monitoring—all using ROS 2's three communication patterns working together. The robot must decide when to use pub-sub (continuous data), services (queries), and actions (goal-oriented tasks) based on each subtask's requirements.

This scenario represents real-world applications in assistive robotics, elder care, and home automation—domains where robots must integrate multiple capabilities safely and reliably. The challenge is choosing the right communication pattern for each part of the task to ensure responsive, safe, and successful execution.

---

### How the Robot Coordinates All Three Patterns

**1. Continuous Perception with Publish-Subscribe (Topics)**

As soon as the command is received, the robot's **vision node** continuously publishes camera images on the `/head_camera/image` topic at 30 frames per second. The **obstacle detection node** subscribes to this stream, processing every frame to detect people, furniture, and dynamic obstacles (like pets). Simultaneously, the **battery monitor** publishes current charge level on `/battery_status` every second, and **joint state publishers** broadcast arm and leg positions continuously.

- **Pattern Used**: Publish-Subscribe (Topics)
- **Why This Pattern**: Vision, obstacle detection, battery monitoring, and joint states are continuous data streams that multiple nodes need simultaneously. Pub-sub enables parallel processing—navigation, safety monitoring, and state estimation all receive the same sensor data without the camera node knowing about each subscriber. This is too frequent and multi-consumer for services or actions.

**2. Pre-Navigation Safety Check with Service (Request-Response)**

Before moving, the robot's **task coordinator** calls the "check_path_feasibility" service, providing start position (current location) and goal position (kitchen). The **path planning node** (service server) receives this request, quickly computes whether a collision-free path exists, and responds within 200 milliseconds: either "feasible: path found" with estimated travel time, or "infeasible: obstacle blocking" with reason. The coordinator waits for this response before proceeding.

- **Pattern Used**: Service
- **Why This Pattern**: Path feasibility is a one-time query requiring a definitive answer before navigation begins. The robot needs to know "Can I reach the kitchen?" right now—not a continuous stream of maybe-paths, and not a long-running navigation process yet. Services provide this quick, synchronous question-and-answer interaction. If the service returns "infeasible," the robot can ask for help instead of attempting impossible navigation.

**3. Navigation to Kitchen with Action (Long-Running Goal)**

With path confirmed feasible, the robot sends a "navigate_to_pose" action goal to the **navigation system**: "move to kitchen coordinates (X: 5.2m, Y: 3.1m)." The navigation system accepts the goal and begins executing. Every second, it sends feedback: "distance remaining: 4.1m, 30% complete," "distance remaining: 2.7m, 55% complete," "approaching goal, 90% complete." The task coordinator monitors this feedback, displaying progress to the user. If the person changes their mind mid-navigation, the coordinator can cancel (preempt) the action. After 15 seconds, the navigation system sends the final result: "success: arrived at goal, final position error: 0.03m."

- **Pattern Used**: Action
- **Why This Pattern**: Navigation takes 10-20 seconds—too long to block with a service call. The robot needs progress updates to show status, detect stalls, and enable cancellation if circumstances change (person says "never mind" or obstacle suddenly appears). Actions provide feedback, preemption, and asynchronous execution, allowing the coordinator to monitor battery levels and obstacle alerts simultaneously while navigation runs.

**4. Grasping the Cup with Action (Manipulation Goal)**

Now in the kitchen, the robot sends a "grasp_object" action to its **manipulation controller**: "grasp cup at detected position (X: 5.3m, Y: 3.2m, Z: 0.9m)." The controller accepts, provides feedback ("moving arm: 40%," "opening gripper: 70%," "closing around object: 95%"), and returns result after 8 seconds: "success: object grasped, grip force: 12N" (confirming secure hold). Throughout, the robot continues subscribing to camera and force sensor topics (pub-sub) for real-time adjustments.

- **Pattern Used**: Action (grasping) + Pub-Sub (sensors during grasp)
- **Why This Pattern**: Grasping is goal-oriented (8 seconds, needs completion confirmation) but also requires continuous sensory feedback (force sensors, vision) via pub-sub. Combining patterns enables sophisticated behavior—the action tracks grasp progress while subscribed sensor topics enable reactive adjustments if the cup shifts.

---

### Expected Outcomes

**What Happens:**

The home assistant successfully fetches the water by using each communication pattern appropriately:
- **Pub-sub** provides continuous perception (vision, obstacles, battery) throughout the entire task
- **Service** confirms path feasibility before committing to navigation, avoiding impossible tasks
- **Actions** execute long-running navigation and grasping with progress feedback and cancellation capability

**Pattern Selection Benefits:**

Choosing the right pattern for each subtask enabled the robot to be responsive (monitor and react to sensor data continuously), efficient (query feasibility quickly without subscribing to path-planning streams), and goal-driven (track multi-second navigation and grasping to completion). Using only pub-sub would lack completion tracking; using only services would block for 20+ seconds; using only actions would be overkill for simple queries.

---

### Real-World Applications

This integrated pattern usage demonstrates capabilities across Physical AI domains:

- **Healthcare Robotics**: Hospital robots deliver medications using pub-sub (patient monitoring), services (medication availability checks), and actions (navigate to room, hand over medicine)
- **Warehouse Automation**: Fulfillment robots pick items using pub-sub (conveyor sensors), services (inventory database queries), and actions (navigate to shelf, grasp package)
- **Manufacturing**: Assembly robots build products using pub-sub (part position tracking), services (tool availability checks), and actions (multi-step assembly sequences with force feedback)

The fundamental principle—match communication pattern to task characteristics (continuous vs one-time vs goal-oriented)—powers all Physical AI applications. Whether the robot assists humans at home, picks packages in warehouses, or assembles products in factories, ROS 2's three patterns working together enable the coordinated intelligence that defines modern robotics.

---

**Word Count**: ~550 words

---

## Chapter Summary

### Key Concepts Recap

In this chapter, you learned how ROS 2 provides three complementary communication patterns to coordinate robot behaviors:

- **Publish-Subscribe (Topics)**: For continuous data streams like sensor readings and state updates—publishers broadcast, subscribers receive, enabling parallel processing and real-time perception throughout robot operation.

- **Services**: For synchronous request-response queries where the robot needs a definitive answer before proceeding—like asking "Is the path feasible?" or "What's the battery level?" The client waits for the server's response, ensuring critical information is received.

- **Actions**: For long-running, goal-oriented tasks that provide progress feedback and support cancellation—like navigation (15 seconds with distance updates) or manipulation (8 seconds with gripper position feedback). Actions enable responsive, interruptible behaviors essential for Physical AI.

### When to Use Each Pattern

**Quick Decision Guide:**
- **Continuous data** (30 Hz sensors, real-time state) → **Pub-Sub**
- **Quick query** (path check, status request, &lt;1 second) → **Service**
- **Long-running goal** (navigation, grasping, &gt;3 seconds) → **Action**

### Important Terms Introduced

- **Service**: Synchronous request-response communication pattern
- **Action**: Asynchronous goal-oriented pattern with feedback
- **Synchronous**: Blocking operation that waits for completion
- **Asynchronous**: Non-blocking operation allowing parallel work
- **Request-Response**: Query pattern where client asks, server answers
- **Goal**: Desired outcome sent to action server
- **Feedback**: Progress updates during action execution
- **Preemption**: Canceling a running action mid-execution
- **Client**: Node requesting service or sending action goal
- **Server**: Node providing service or executing action

**Quick Reference**: If you encounter these terms in later chapters and need a refresher, refer back to the Concept Explanation section of this chapter.

### How This Chapter Fits

This chapter is part of **Module 1: The Robotic Nervous System (ROS 2)**.

**What you've accomplished in Module 1**:
- ✅ Chapter 1: Understood ROS 2 architecture, nodes, topics, and the distributed nervous system concept
- ✅ Chapter 2: Learned publish-subscribe pattern for continuous data streaming
- ✅ Chapter 3: Mastered services and actions for queries and goal-oriented behaviors (this chapter)

**Module Progress**: You've completed **all 3 chapters** in Module 1 (100%)!

**Big Picture**: Module 1 equipped you with ROS 2's complete communication toolkit. Chapter 1 introduced the nervous system architecture, Chapter 2 deep-dived into pub-sub for sensor streams, and Chapter 3 added services (queries) and actions (goals) to complete the pattern trio. The home assistant example showed all three patterns working together—continuous perception (pub-sub), feasibility checks (service), and navigation/grasping (actions). You now understand how Physical AI systems coordinate sensing, planning, and execution through ROS 2's layered communication patterns.

### What's Next: Module 2

In the next module, **Digital Twin & Simulation**, you'll build on your ROS 2 communication knowledge to explore:

- How digital twins create virtual replicas of physical robots for safe testing before deployment
- Simulation environments (Gazebo, Unity) that use ROS 2 pub-sub, services, and actions virtually
- Why testing navigation, grasping, and multi-robot coordination in simulation saves time and prevents real-world accidents
- The sim-to-real transfer process that moves validated behaviors from virtual to physical robots

**Why this matters**: Simulation is how robotics professionals develop safely and efficiently—you'll see the same pub-sub/service/action patterns from Module 1 applied to virtual robots, enabling rapid iteration without hardware damage risks.

**Get ready to**: Explore how simulated humanoid robots use the exact communication patterns you've mastered to navigate virtual kitchens and grasp virtual objects!

### Congratulations!

Excellent work completing Module 1! You've mastered ROS 2's complete communication foundation—from basic architecture to pub-sub continuous streaming to services and actions for queries and goals. You now understand the robotic nervous system that powers modern Physical AI. Module 2 will show you how to apply these patterns in simulation environments before deploying to real hardware. Keep going—you're building strong fundamentals!

---

**Word Count**: ~290 words

---
