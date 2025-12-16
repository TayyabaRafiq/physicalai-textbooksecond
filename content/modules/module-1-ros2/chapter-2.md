---
sidebar_position: 2
---

# Chapter 2: Nodes, Topics, and Message Passing

**Estimated Reading Time**: 25 minutes
**Lab Duration**: 40-50 minutes

---

## Concept Explanation: Understanding ROS 2 Communication Patterns

### Introduction

In Chapter 1, you learned that ROS 2 acts as a "robotic nervous system," enabling independent programs (nodes) to coordinate through named communication channels (topics). You saw talker and listener nodes exchanging messages and visualized their connections with rqt_graph. But how exactly do nodes send and receive data? What are messages, and how do they carry information between robot components?

This chapter dives deeper into ROS 2 communication mechanisms. You'll learn how **publishers** send data, how **subscribers** receive it, what **messages** contain, and how **Quality-of-Service (QoS)** settings control message delivery. By the end, you'll understand the publish-subscribe pattern that powers all ROS 2 robot systems—from simple sensors to complex humanoid behaviors. This knowledge is essential for building your own nodes that coordinate sensing, planning, and action in Physical AI systems.

---

### Key Concepts

#### Publishers: Sending Data on Topics

**Publisher**: A node that sends (publishes) data on a specific topic at regular intervals or in response to events, making information available to any interested subscribers.

**In Plain English**: Think of a publisher like a weather station broadcasting temperature readings. The station doesn't know who's listening—it just keeps transmitting measurements on a radio frequency (the topic). Anyone with a radio tuned to that frequency can hear the updates. Similarly, a camera node publishes images on a topic like `/camera/image`, and any node needing those images can subscribe to receive them.

**Why It Matters**: Publishers enable sensors and data sources to make information available without worrying about who uses it. A lidar sensor can publish distance measurements, and whether one node, ten nodes, or zero nodes subscribe doesn't affect the publisher. This **decoupling** (independence between sender and receiver) makes robot systems flexible—you can add new components without modifying existing ones.

**Example**: A robot arm's joint state publisher continuously broadcasts current joint angles on the `/joint_states` topic at 50 Hz (50 times per second). The robot's visualization system subscribes to display the arm's position, the motion planner subscribes to check for collisions, and a data recorder subscribes to log the trajectory. The joint state publisher doesn't know about these three subscribers—it just publishes data, and interested nodes receive it.

---

#### Subscribers: Receiving Data from Topics

**Subscriber**: A node that receives (subscribes to) data from a specific topic, processing each incoming message through a callback function whenever new data arrives.

**In Plain English**: Think of a subscriber like a smartphone app that receives notifications. When someone sends you a message, your phone's messaging app gets notified and displays it—you don't have to constantly check for new messages. Similarly, when a publisher sends data on a topic, all subscribers automatically receive it through their callback functions. The subscriber doesn't poll (repeatedly check) for updates; ROS 2's middleware delivers messages as they arrive.

**Why It Matters**: Subscribers enable nodes to react to data in real-time. When a camera publishes a new image, the object detection subscriber immediately processes it. When the planner publishes a new velocity command, the motor controller subscriber immediately executes it. This **event-driven** approach (reacting when data arrives) is more efficient than constantly checking if new data exists, and it's essential for real-time robot control where timing matters.

**Example**: A warehouse robot's obstacle avoidance node subscribes to the `/scan` topic to receive lidar data. Every 100 milliseconds, when new distance measurements arrive, the subscriber's callback function runs, checking if any obstacles are closer than 0.5 meters. If an obstacle is detected, the callback publishes a stop command on the `/cmd_vel` topic. The subscriber doesn't run continuously checking for data—it only activates when new lidar scans arrive.

---

#### Messages: Structured Data Packets

**Message**: A structured data packet with defined fields and types (like integers, floats, strings, arrays) that carries information between publishers and subscribers on a topic.

**In Plain English**: Think of a message like a form with specific fields. A weather form might have fields for "temperature (number)", "humidity (number)", "conditions (text)", and "timestamp (date/time)". Everyone using that form knows exactly what information it contains and where to find each piece. Similarly, a ROS 2 message type like `sensor_msgs/Image` has fields for "height (integer)", "width (integer)", "encoding (string)", and "data (byte array)". When a camera publishes an image message, subscribers know exactly how to extract the width, height, and pixel data.

**Why It Matters**: Messages ensure publishers and subscribers speak the same language. A camera node can publish images with confidence that any image subscriber—whether it's for object detection, face recognition, or recording—will correctly interpret the data. Without standardized message types, every sensor would need custom code for every consumer, making robot systems impossibly complex. ROS 2 provides hundreds of pre-defined message types (sensor data, geometry, navigation commands) so you don't have to design data structures from scratch.

**Example**: A GPS sensor publishes location data using the `sensor_msgs/NavSatFix` message type. This message has fields like `latitude` (double), `longitude` (double), `altitude` (double), and `status` (integer indicating GPS signal quality). A mapping node subscribing to this data can access `msg.latitude` to get the current position, and a navigation planner can check `msg.status` to verify GPS signal is strong before trusting the position estimate. All nodes using `NavSatFix` messages interpret the data identically.

---

#### Publish-Subscribe Pattern: Many-to-Many Communication

**Publish-Subscribe Pattern**: A communication design where publishers send data to topics without knowing who (if anyone) is listening, and subscribers receive data from topics without knowing who sent it, enabling flexible many-to-many connections.

**In Plain English**: Think of a publish-subscribe system like a newspaper. The publisher (newspaper company) prints articles and distributes them without knowing exactly who will read each section. Readers (subscribers) pick up the newspaper and read the sections they care about (sports, business, local news) without knowing who wrote each article or who else is reading. The newspaper company doesn't need permission from readers to publish, and readers don't need to register with specific writers to receive content.

**Why It Matters**: The pub-sub pattern is what makes ROS 2 systems so flexible and scalable. You can add a new sensor (publisher) without modifying any existing nodes—interested nodes just subscribe to the new topic. You can add a new data consumer (subscriber) without modifying the sensor—it just starts receiving data. Multiple nodes can publish on the same topic (sensor fusion combining multiple cameras), and multiple nodes can subscribe to one topic (many systems needing the same sensor data). This **loose coupling** (minimal dependencies between components) makes robot systems easier to develop, test, and extend.

**Example**: A humanoid robot's camera publishes images on `/head_camera/image`. Five different nodes subscribe: (1) face detection for human-robot interaction, (2) object recognition for grasping, (3) visual odometry for localization, (4) data recording for later analysis, and (5) a web interface for remote viewing. The camera doesn't know these five subscribers exist. Later, you add a sixth subscriber for gesture recognition—no changes needed to the camera node or the other five subscribers. When you temporarily disable the object recognition node for debugging, the camera keeps publishing and the other four subscribers keep working. This independence enables rapid development and fault tolerance.

---

#### Quality-of-Service (QoS): Controlling Message Delivery

**Quality-of-Service (QoS)**: Configuration settings that control how messages are delivered between publishers and subscribers, specifying reliability (guaranteed vs best-effort), durability (store for late-joining subscribers), history (how many messages to keep), and deadline (maximum time between messages).

**In Plain English**: Think of QoS like choosing mail delivery options. Regular mail (best-effort) is cheap and fast, but letters might get lost. Certified mail (reliable) guarantees delivery but costs more and is slower. Priority mail (deadline) promises delivery within specific timeframes. You can also request mail forwarding (durability) so new residents at an address get previously sent letters. Similarly, ROS 2 lets you configure how messages are delivered based on what your application needs.

**Why It Matters**: Different robot systems have different needs. A safety-critical emergency stop command MUST be delivered reliably—you can't afford lost messages. But streaming camera images at 30 frames per second can use best-effort delivery—if one frame drops, the next frame arrives in 33 milliseconds anyway. A mapping node joining a running system might need durability (receive the last published map even if it was sent before subscription). A watchdog timer might need deadline settings (alert if messages stop arriving). QoS policies let you match message delivery to your specific requirements without changing code—just configuration.

**Example**: A robot arm's joint command topic uses "reliable" QoS (like certified mail) because missing a command could cause erratic motion or collisions. The DDS middleware will re-transmit any lost messages until confirmed received. In contrast, the same robot's joint state topic (current positions) uses "best-effort" QoS (like regular mail) because joint states are published at 100 Hz—if one message is lost, the next arrives in 10 milliseconds. A lidar sensor might use "transient local" durability, storing the last published scan so nodes that start late (after the robot is already running) immediately receive the most recent data instead of waiting for the next scan.

---

[DIAGRAM: Publish-Subscribe Communication Flow]
- Elements to show: Publisher node → Topic (named channel) → Multiple Subscriber nodes (1, 2, 3)
- Labels needed: Publisher, Topic name ("/sensor/data"), Subscribers, Message type (sensor_msgs/LaserScan), Data flow arrows (publisher → topic → subscribers)
- Purpose: Visualize how one publisher sends messages to multiple subscribers through a topic, with no direct connections between nodes

---

### Transition to Example

Now that you understand how publishers send data, subscribers receive it, messages carry structured information, the publish-subscribe pattern enables flexible many-to-many communication, and QoS settings control delivery—let's see these concepts in action. The next section demonstrates a robot vision system where a camera node publishes images, and multiple specialized nodes subscribe to process those images for different purposes. You'll see how the pub-sub pattern enables parallel processing and fault isolation in a real Physical AI application.

---

**Word Count**: ~1,100 words

---

## Example: Security Robot Vision System with Multiple Subscribers

### Scenario: Autonomous Security Patrol

Imagine a mobile security robot patrolling an office building at night. The robot's camera captures video of hallways, lobbies, and entrance areas to detect intruders, monitor for safety hazards (like water leaks or fallen objects), and verify that doors are properly closed. A single camera produces 30 images per second, but multiple different systems need to process these images simultaneously for different purposes.

This scenario represents real-world applications in security automation, facility management, and safety monitoring—domains where one sensor's data must serve multiple purposes without creating bottlenecks or requiring custom connections for each use case. The challenge is enabling parallel processing while maintaining system flexibility and fault tolerance.

---

### How the Robot Solves This Challenge

**1. Camera Publishes Image Stream**

The **camera_node** captures images from the security robot's camera at 30 frames per second. Instead of sending images directly to specific processing nodes, it publishes each image as a `sensor_msgs/Image` message on the `/security/camera` topic. The camera doesn't know (or care) how many nodes are listening—it just continuously publishes images whenever they're captured.

- **Concept Applied**: Publisher (from concept section)
- **In Action**: The camera_node acts as a weather station broadcasting data. It publishes 640x480 RGB images with timestamp metadata, making them available on a named topic. Whether zero nodes, three nodes, or ten nodes subscribe doesn't affect the camera's operation.

**2. Object Detection Subscribes for Intrusion Monitoring**

An **object_detector_node** subscribes to `/security/camera` to identify people in the video feed. When a new image message arrives, its callback function runs a computer vision algorithm to detect human shapes. If a person is detected after business hours (when the building should be empty), the node publishes an alert on the `/security/alert` topic.

- **Concept Applied**: Subscriber with callback function (from concept section)
- **In Action**: The object detector doesn't poll for images—it reacts when messages arrive (event-driven). Each of the 30 images per second triggers the callback, which processes the image and decides whether to raise an alarm. This subscriber receives exactly the same image data as all other subscribers.

**3. Hazard Detection Subscribes for Safety Monitoring**

Simultaneously, a **hazard_detector_node** also subscribes to `/security/camera`. Its callback analyzes images for water on floors (shiny reflections), fallen objects blocking pathways, or smoke. When hazards are detected, it publishes warnings on the `/safety/hazard` topic. This node runs completely independently of the object detector—if the object detector crashes, hazard detection continues unaffected.

- **Concept Applied**: Many-to-many publish-subscribe pattern (from concept section)
- **In Action**: Both object_detector and hazard_detector subscribe to the same camera topic, demonstrating **one publisher, multiple subscribers**. The camera publishes once; two nodes receive the data. Neither subscriber knows about the other, and they process images in parallel without interfering.

**4. Recording Subscribes for Evidence Archive**

A third node, **video_recorder_node**, subscribes to `/security/camera` to save all footage to disk for later review. Its callback simply writes each image to a video file with timestamp. This recorder operates passively—it doesn't analyze images or publish alerts, just archives data.

- **Concept Applied**: Loose coupling and fault isolation (from pub-sub pattern concept)
- **In Action**: Adding this third subscriber required NO changes to the camera node, object detector, or hazard detector. The recorder just starts subscribing, and it immediately receives camera data. If recording fails (disk full), the camera keeps publishing and the other two subscribers keep working. This independence enables robust systems.

---

### Expected Outcomes

**What Happens:**

The security robot successfully monitors the building with all three systems processing camera data in parallel. Key success indicators include:

- **Parallel Processing**: Object detection, hazard detection, and recording all happen simultaneously at 30 FPS without the camera knowing about any subscribers
- **Fault Isolation**: When the hazard detector is temporarily disabled for software updates, intrusion monitoring and recording continue unaffected
- **Scalability**: Later, a fourth subscriber is added for facial recognition to verify employee access—no modifications needed to existing nodes

**Without Publish-Subscribe:**

If the camera sent images directly to each consumer (point-to-point connections), adding the third subscriber (recorder) would require modifying the camera code to create another connection. If one subscriber crashed, it could block the camera from sending to others. Processing would be sequential (one node at a time) instead of parallel. The pub-sub pattern avoids all these problems.

---

### Real-World Applications

This vision system example demonstrates publish-subscribe patterns used across Physical AI domains:

- **Manufacturing Automation**: Factory inspection cameras publish images to defect detection (quality control), part counting (inventory), and compliance recording (audit trails) simultaneously
- **Autonomous Vehicles**: Self-driving cars publish lidar scans to obstacle detection (safety), mapping (localization), and data logging (development) without creating bottlenecks
- **Healthcare Robotics**: Surgical robots publish instrument position data to visualization (surgeon display), collision detection (safety), and training recording (medical education) in parallel

The fundamental concepts—publishers broadcasting data, subscribers receiving through callbacks, messages carrying structured information, and loose coupling enabling parallel processing—power all these applications. Whether the robot monitors security, assembles products, or drives passengers, ROS 2's publish-subscribe pattern coordinates sensing and decision-making in Physical AI systems.

---

**Word Count**: ~520 words

---

## Chapter Summary

### Key Concepts Recap

In this chapter, you learned how ROS 2 nodes actually communicate to coordinate robot behaviors:

- **Publishers**: Nodes that broadcast data on topics without knowing who's listening, enabling sensors and data sources to make information available flexibly—like a weather station transmitting readings for anyone to receive.

- **Subscribers**: Nodes that receive data from topics through event-driven callback functions, reacting immediately when new messages arrive instead of constantly polling for updates—essential for real-time robot control.

- **Messages**: Standardized data packets with defined fields (integers, floats, strings, arrays) that ensure publishers and subscribers speak the same language, preventing the chaos of custom formats for every sensor-consumer pair.

- **Publish-Subscribe Pattern**: The communication design where publishers and subscribers don't know about each other directly, communicating only through named topics—this loose coupling enables you to add sensors or data consumers without modifying existing nodes.

- **Quality-of-Service (QoS)**: Configuration settings that control message delivery (reliability, durability, history, deadlines), letting you match communication behavior to application needs—reliable delivery for critical commands, best-effort for high-frequency sensor streams.

### Important Terms Introduced

- **Publisher**: A node that sends data on a specific topic
- **Subscriber**: A node that receives data from a specific topic through callbacks
- **Message**: Structured data packet with defined fields and types
- **Callback Function**: Code that runs automatically when a subscriber receives new data
- **Publish-Subscribe Pattern**: Communication design with loose coupling through topics
- **Decoupling**: Independence between sender and receiver
- **Loose Coupling**: Minimal dependencies between components
- **Event-Driven**: Reacting when data arrives rather than constantly checking
- **Quality-of-Service (QoS)**: Settings controlling message delivery guarantees
- **Reliability**: QoS setting for guaranteed vs best-effort message delivery
- **Durability**: QoS setting for storing messages for late-joining subscribers

**Quick Reference**: If you encounter these terms in later chapters and need a refresher, refer back to the Concept Explanation section of this chapter.

### How This Chapter Fits

This chapter is part of **Module 1: The Robotic Nervous System (ROS 2)**.

**What you've accomplished so far**:
- ✅ Chapter 1: Understood ROS 2 architecture and the concept of nodes/topics at a high level
- ✅ Chapter 2: Learned how nodes communicate through publishers, subscribers, and messages (this chapter)

**Module Progress**: You've completed 2 of 3 chapters in Module 1.

**Big Picture**: Chapter 1 introduced ROS 2 as the robot's nervous system, explaining *what* nodes and topics are. Chapter 2 dove deeper into *how* that nervous system works—publishers broadcasting data, subscribers receiving through callbacks, messages carrying structured information, and QoS controlling delivery. The security robot example showed these concepts enabling parallel processing and fault isolation in a real system. The next chapter brings this all together by showing ROS 2 controlling simulated robots in Gazebo, giving you hands-on experience with complete robot systems where you'll see publishers, subscribers, and messages coordinating virtual sensors and motors.

### What's Next: Chapter 3

In the next chapter, **ROS 2 Simulation with Gazebo**, you'll build on what you've learned here to explore:

- How Gazebo creates virtual robot environments with realistic physics and sensors
- How simulated robots publish sensor data (lidar, cameras) to ROS 2 topics—exactly like the publishers you learned about
- How to control robot movement by publishing velocity commands to topics—applying the pub-sub pattern hands-on
- Why simulation enables safe, cheap experimentation before deploying to physical hardware

**Why this matters**: Simulation is how robotics professionals develop and test systems—you'll experience the complete workflow of sensing, planning, and acting in a virtual robot.

**Get ready to**: Drive a simulated Turtlebot through a Gazebo world using the ROS 2 publisher and subscriber concepts you've mastered!

### You're Making Progress!

Excellent progress! You're now 67% through Module 1 (2 of 3 chapters complete). The concepts are building on each other—you started by understanding ROS 2's architecture, then learned how communication actually works through publishers and subscribers. The upcoming simulation chapter will let you apply these skills hands-on. Keep going—each chapter brings you closer to mastering the robotic nervous system!

---

**Word Count**: ~280 words

---
