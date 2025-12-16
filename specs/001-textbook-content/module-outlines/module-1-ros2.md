# Module 1: The Robotic Nervous System (ROS 2)

**Module Number**: 1 of 4
**Priority**: P1 (Foundation - must complete before other modules)
**Estimated Duration**: 2.5-4 hours (reading + labs)

## Module Overview

This foundational module introduces ROS 2 (Robot Operating System 2) as the "nervous system" of modern robots. Learners will understand how robots coordinate sensing, planning, and action through distributed communication systems. The module uses simulation-first approach with Gazebo to avoid hardware requirements.

## Learning Objectives

By the end of this module, learners will be able to:

1. **Explain** the role of ROS 2 in robot systems and why distributed communication is essential for Physical AI
2. **Describe** the core ROS 2 concepts: nodes, topics, messages, publishers, subscribers, and services
3. **Demonstrate** understanding of ROS 2 architecture through hands-on simulation exercises in Gazebo
4. **Recognize** how ROS 2 enables coordination between robot perception, planning, and control systems

## Prerequisites

- **Technical Background**: Basic programming knowledge (any language) helpful but not required
- **Prior Robotics**: None - module designed for complete beginners
- **Software**: Access to Linux system or VM for ROS 2 installation (guided in labs)

## Module Structure

---

### Chapter 1: ROS 2 Basics and Architecture

**Learning Goals**:
- Understand what ROS 2 is and why it's essential for modern robotics
- Explain the distributed architecture of ROS 2 systems
- Identify the key components of a ROS 2 ecosystem

**Key Concepts**:
- ROS 2 as a robot "nervous system"
- Distributed vs. centralized robot control
- The ROS 2 graph: nodes and connections
- Communication middleware (DDS)

**Example**: "Robot Delivery System"
- Scenario: A package delivery robot coordinating camera, navigation, and wheels
- Demonstrates how ROS 2 enables independent components to work together
- Shows value of distributed communication

**Lab Activity**: "Install ROS 2 and Explore the Environment"
- **Objective**: Set up ROS 2 environment and run first commands
- **Tools**: ROS 2 Humble (LTS), Linux terminal
- **Duration**: 45-60 minutes
- **Steps**:
  1. Install ROS 2 Humble (guided with script)
  2. Source ROS 2 environment
  3. Run demo nodes (talker/listener)
  4. Visualize ROS 2 graph with rqt_graph
  5. Explore running nodes and topics
- **Expected Outcomes**: Learner sees nodes communicating and understands basic ROS 2 structure

**Exercises**:
1. What problem does ROS 2 solve for robot systems?
2. Why is a distributed architecture beneficial for robots?
3. How does the ROS 2 graph help visualize robot systems?
4. Compare centralized control vs. ROS 2 distributed approach

---

### Chapter 2: Nodes, Topics, and Message Passing

**Learning Goals**:
- Define ROS 2 nodes and explain their role in robot systems
- Understand topic-based communication patterns
- Describe how publishers and subscribers work together
- Explain message types and data flow in ROS 2

**Key Concepts**:
- **Nodes**: Independent processes performing specific tasks
- **Topics**: Named channels for data communication
- **Publishers**: Nodes that send data on topics
- **Subscribers**: Nodes that receive data from topics
- **Messages**: Structured data packets (e.g., sensor readings, commands)
- **Many-to-many communication**: Multiple publishers/subscribers per topic

**Example**: "Robot Vision System"
- Scenario: Camera node publishing images, multiple nodes subscribing (object detection, recording, display)
- Demonstrates topic-based publish/subscribe pattern
- Shows why this pattern scales better than point-to-point communication

**Lab Activity**: "Create Your First ROS 2 Publisher and Subscriber"
- **Objective**: Understand data flow by observing topic communication
- **Tools**: ROS 2 command-line tools (ros2 topic, ros2 node)
- **Duration**: 40-50 minutes
- **Steps**:
  1. List active topics in a running ROS 2 system
  2. Echo (listen to) a topic to see messages
  3. Publish test messages to a topic using command line
  4. Run a simple publisher node (provided Python script)
  5. Run a subscriber node that reacts to messages
  6. Observe many-to-many communication patterns
- **Expected Outcomes**: Learner sees how nodes communicate via topics without direct connections

**Exercises**:
1. What is a ROS 2 node and what role does it play?
2. How does topic-based communication differ from function calls?
3. Why can multiple nodes subscribe to the same topic?
4. When would you use a topic vs. a direct connection between nodes?

---

### Chapter 3: ROS 2 Simulation with Gazebo

**Learning Goals**:
- Understand the role of simulation in robot development
- Explain how Gazebo integrates with ROS 2
- Demonstrate basic robot control in a simulated environment
- Recognize benefits of simulation-first development

**Key Concepts**:
- **Gazebo**: 3D robot simulator with physics engine
- **Simulation vs. Real Hardware**: Why simulate first
- **Sensor Simulation**: Camera, lidar, IMU in virtual environment
- **ROS 2 + Gazebo Integration**: Topics bridging sim and ROS 2
- **URDF**: Robot description format (conceptual overview only)

**Example**: "Simulated Turtlebot Navigation"
- Scenario: Turtlebot3 robot navigating a simple environment in Gazebo
- Demonstrates sensor data (lidar) flowing through ROS 2 topics
- Shows how simulation enables safe experimentation

**Lab Activity**: "Launch and Control a Simulated Robot"
- **Objective**: Experience ROS 2 + Gazebo integration hands-on
- **Tools**: Gazebo, ROS 2 Humble, Turtlebot3 packages
- **Duration**: 50-60 minutes
- **Steps**:
  1. Install Gazebo and Turtlebot3 simulation packages
  2. Launch Turtlebot3 world in Gazebo
  3. Observe topics published by simulated robot
  4. Subscribe to camera and lidar topics to see sensor data
  5. Publish velocity commands to move the robot
  6. Experiment with basic navigation commands
- **Expected Outcomes**: Learner controls a simulated robot using ROS 2 topics, reinforcing module concepts

**Exercises**:
1. Why is simulation valuable for robot development?
2. How does Gazebo integrate with ROS 2 systems?
3. What types of sensors can be simulated in Gazebo?
4. Compare testing a robot in simulation vs. on physical hardware

---

## Module Summary

**Key Takeaways**:
- ROS 2 is the distributed "nervous system" enabling robot components to communicate
- Nodes are independent processes; topics are named data channels
- Publishers send data, subscribers receive data, enabling flexible many-to-many communication
- Simulation with Gazebo allows safe, cost-effective robot development before physical deployment

**Technical Terms Introduced**:
- ROS 2, Node, Topic, Publisher, Subscriber, Message, DDS, Gazebo, URDF, Turtlebot

**Transition to Module 2**:
Now that you understand how robots communicate using ROS 2, Module 2 will explore Digital Twins and Simulation in greater depth. You'll learn how to create virtual replicas of physical robots and test AI behaviors safely before deployment.

---

## Module Validation Checklist

- [ ] All 3 chapters cover ROS 2 fundamentals (FR-009)
- [ ] ROS 2 explained as "robotic nervous system" (FR-010)
- [ ] Hands-on labs use ROS 2 simulation tools (Gazebo) (FR-011)
- [ ] Content accessible to beginners without prior robotics knowledge (FR-005)
- [ ] No deep mathematical derivations (FR-006)
- [ ] All technical terms defined on first use (FR-021)
- [ ] Module can stand alone as foundational ROS 2 introduction (SC-005)