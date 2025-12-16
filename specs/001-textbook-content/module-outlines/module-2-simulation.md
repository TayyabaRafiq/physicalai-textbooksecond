# Module 2: Digital Twin & Simulation (Gazebo / Unity)

**Module Number**: 2 of 4
**Priority**: P2 (Builds on Module 1 - ROS 2 foundation)
**Estimated Duration**: 2.5-4 hours (reading + labs)

## Module Overview

This module explores digital twins and simulation environments for Physical AI development. Learners will understand how to create virtual replicas of physical robots, test behaviors safely in simulation, and leverage both Gazebo and Unity platforms. The simulation-first approach enables AI experimentation without expensive hardware.

## Learning Objectives

By the end of this module, learners will be able to:

1. **Define** digital twins and explain their role in Physical AI development
2. **Describe** the benefits of simulation-first robot development
3. **Compare** Gazebo and Unity as robot simulation platforms
4. **Demonstrate** creating basic simulated robot environments with physics and sensors
5. **Recognize** how simulation enables safe AI behavior testing before physical deployment

## Prerequisites

- **Prior Modules**: Module 1 (ROS 2 Basics) - REQUIRED
- **Technical Background**: Understanding of ROS 2 nodes and topics
- **Software**: Gazebo (from Module 1), Unity Hub (free), basic familiarity with 3D environments helpful

## Module Structure

---

### Chapter 1: Digital Twin Concepts for Physical AI

**Learning Goals**:
- Understand what a digital twin is and how it differs from traditional simulation
- Explain why digital twins are critical for Physical AI development
- Identify the components of a robot digital twin
- Recognize use cases where digital twins provide value

**Key Concepts**:
- **Digital Twin**: Virtual replica that mirrors physical system behavior
- **Simulation vs. Digital Twin**: Real-time sync vs. sandbox testing
- **Components**: Geometry, physics, sensors, actuators, environment
- **Sim-to-Real Transfer**: Training AI in simulation, deploying on physical robot
- **Digital Twin Benefits**: Safety, cost, scalability, parallel testing

**Example**: "Warehouse Robot Digital Twin"
- Scenario: Creating a digital twin of a warehouse picking robot
- Demonstrates how virtual model mirrors real robot sensors and movements
- Shows value of testing collision avoidance in simulation first

**Lab Activity**: "Explore an Existing Digital Twin"
- **Objective**: Understand digital twin components by examining a complete example
- **Tools**: Gazebo, ROS 2, pre-built robot model (Turtlebot3 or similar)
- **Duration**: 40-50 minutes
- **Steps**:
  1. Launch a detailed robot model in Gazebo
  2. Examine the robot's simulated sensors (camera, lidar, IMU)
  3. Observe how sensor data matches physical sensor characteristics
  4. Test the physics engine (collisions, gravity, friction)
  5. Compare simulated sensor noise to real-world expectations
  6. Modify environment and observe robot responses
- **Expected Outcomes**: Learner sees how digital twins capture essential physical robot properties

**Exercises**:
1. What is a digital twin and how does it differ from a basic simulation?
2. Why is simulation critical for Physical AI development?
3. What components must a robot digital twin include?
4. When would you use a digital twin vs. testing on physical hardware?

---

### Chapter 2: Gazebo Simulation Fundamentals

**Learning Goals**:
- Understand Gazebo architecture and ROS 2 integration
- Explain how physics engines simulate real-world robot behavior
- Describe simulated sensors and their data outputs
- Demonstrate creating custom simulation environments

**Key Concepts**:
- **Gazebo Architecture**: World files, models, plugins
- **Physics Engine**: ODE, Bullet, or others for realistic motion
- **Simulated Sensors**: Lidar, cameras, depth sensors, IMU, GPS
- **ROS 2 + Gazebo Bridge**: How topics connect simulation to ROS 2
- **SDF (Simulation Description Format)**: Environment and model definitions
- **Sensor Noise and Accuracy**: Modeling real-world imperfections

**Example**: "Autonomous Navigation Environment"
- Scenario: Building a Gazebo world with obstacles for navigation testing
- Demonstrates how to create environments for specific AI tasks
- Shows sensor data quality and how it affects AI perception

**Lab Activity**: "Build a Custom Gazebo World for Robot Testing"
- **Objective**: Create a simulation environment from scratch
- **Tools**: Gazebo, SDF files, ROS 2
- **Duration**: 50-60 minutes
- **Steps**:
  1. Create a new Gazebo world file
  2. Add ground plane and basic lighting
  3. Insert obstacles and walls for navigation
  4. Spawn a robot model (Turtlebot3)
  5. Verify sensor data is published to ROS 2 topics
  6. Test robot movement and collision detection
  7. Modify environment to create different test scenarios
- **Expected Outcomes**: Learner builds a functional test environment for robot AI

**Exercises**:
1. How does Gazebo integrate with ROS 2 systems?
2. What role does the physics engine play in simulation?
3. Why is sensor noise important to include in simulations?
4. Compare Gazebo world files (SDF) to robot descriptions (URDF)

---

### Chapter 3: Unity for Robot Simulation

**Learning Goals**:
- Understand Unity as an alternative robot simulation platform
- Explain when to choose Unity vs. Gazebo
- Describe Unity's game engine advantages for AI training
- Demonstrate basic robot simulation in Unity

**Key Concepts**:
- **Unity for Robotics**: Game engine adapted for robot simulation
- **Gazebo vs. Unity**: Physics fidelity vs. visual realism and scalability
- **Unity Robotics Hub**: ROS integration tools and packages
- **ML-Agents**: Unity's reinforcement learning framework
- **Photorealistic Rendering**: High-quality visuals for vision AI
- **Parallel Simulation**: Running many simulations simultaneously for AI training

**Example**: "Vision AI Training in Unity"
- Scenario: Training a robot to recognize objects using Unity's photorealistic rendering
- Demonstrates Unity's strengths for vision-based AI tasks
- Shows how parallel simulations accelerate machine learning

**Lab Activity**: "Create a Unity Robot Simulation Environment"
- **Objective**: Experience Unity's approach to robot simulation
- **Tools**: Unity Hub (free), Unity Robotics Hub packages
- **Duration**: 50-60 minutes
- **Steps**:
  1. Install Unity Hub and create new robotics project
  2. Import Unity Robotics Hub packages
  3. Build a simple environment with floor, walls, objects
  4. Import or create a basic robot model
  5. Add simulated camera and observe visual output
  6. Configure physics properties (mass, friction)
  7. Compare Unity's rendering to Gazebo's visuals
- **Expected Outcomes**: Learner understands Unity's simulation capabilities and differences from Gazebo

**Exercises**:
1. What are Unity's key advantages for robot simulation?
2. When would you choose Unity over Gazebo for a project?
3. How does Unity's rendering benefit vision-based AI systems?
4. Explain the concept of parallel simulation for AI training

---

## Module Summary

**Key Takeaways**:
- Digital twins are virtual replicas enabling safe, cost-effective robot AI development
- Gazebo provides physics-accurate simulation tightly integrated with ROS 2
- Unity offers photorealistic rendering and parallel simulation for vision AI training
- Simulation-first development allows testing behaviors before expensive physical deployment
- Different platforms (Gazebo vs. Unity) suit different use cases

**Technical Terms Introduced**:
- Digital Twin, Sim-to-Real, Gazebo, Unity, SDF, Physics Engine, Sensor Noise, Parallel Simulation, Unity Robotics Hub, ML-Agents

**Transition to Module 3**:
With ROS 2 communication (Module 1) and simulation environments (Module 2) understood, Module 3 will introduce AI-driven robot intelligence. You'll learn how NVIDIA Isaac adds perception, planning, and control to create truly autonomous Physical AI systems.

---

## Module Validation Checklist

- [ ] All 3 chapters cover digital twin concepts and their role (FR-012)
- [ ] Content includes both Gazebo and Unity simulation platforms (FR-013)
- [ ] Hands-on labs demonstrate creating simulated robot environments with physics (FR-014)
- [ ] Content accessible to beginners (builds on Module 1 knowledge only) (FR-005)
- [ ] No deep mathematical derivations (e.g., physics engine equations avoided) (FR-006)
- [ ] All technical terms defined on first use (FR-021)
- [ ] Examples use simulation-first approach (no physical hardware) (FR-007)