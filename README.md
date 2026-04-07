Gesture-Based Music Controller

Computer Vision | Human-Computer Interaction | Python

Project Overview

This project is a real-time gesture-controlled music system that enables users to interact with audio playback using only hand movements. By leveraging computer vision and hand-tracking technologies, the system eliminates the need for physical input devices, providing a touchless and intuitive user experience.

The application captures live video input from a webcam, detects hand landmarks, interprets gestures, and translates them into system-level and application-level audio controls.

Objectives
Develop a contactless human-computer interaction system
Implement real-time hand gesture recognition using machine learning tools
Integrate gesture input with multimedia control functions
Design a responsive and informative visual feedback interface (HUD)

System Architecture
The system consists of the following components:

Input Layer
Webcam captures live video stream
Processing Layer
Hand detection and landmark tracking using MediaPipe
Gesture classification based on finger states and distances
Control Layer
Maps recognized gestures to system commands (volume, playback, mute)
Output Layer
Audio playback via Pygame
Real-time Heads-Up Display (HUD) using OpenCV


Technologies & Tools
Python – Core programming language
OpenCV – Real-time image processing and rendering
MediaPipe – Hand tracking and landmark detection
Pygame – Audio playback engine
Tkinter – File selection interface
ctypes (Windows API) – System volume control integration


Key Features
Gesture-Based Volume Control
Uses the distance between thumb and index finger to dynamically adjust volume levels.
Playback Control via Hand Gestures
Fist gesture toggles play/pause
Peace sign toggles mute/unmute
Real-Time Visual Feedback (HUD)
Displays system status including:
Current track name
Playback state
Volume percentage
Detected gesture
Dynamic Audio Integration
Allows users to load and play local music files with continuous looping support.


Technical Highlights
Implemented finger state detection algorithm using landmark comparison
Utilized Euclidean distance mapping for smooth volume interpolation
Designed a debouncing mechanism to prevent repeated gesture triggering
Integrated system-level key events for hardware volume control
Optimized for real-time performance with minimal latency


Challenges & Solutions
Gesture Misclassification
→ Addressed using threshold tuning and finger state validation
Volume Sensitivity Control
→ Applied interpolation and change thresholds to stabilize adjustments
User Experience Clarity
→ Implemented a semi-transparent HUD for intuitive feedback


Potential Enhancements
Multi-hand gesture support
Gesture-based track navigation (next/previous)
Cross-platform system control (Linux/macOS)
Integration with streaming services (Spotify API)
Deployment as a desktop application with GUI


Impact
This project demonstrates the practical application of computer vision in human-computer interaction, particularly in creating touchless control systems. It is relevant for environments where physical interaction is limited or undesirable, such as smart homes, accessibility tools, and interactive installations.

Role
Full Project Developer

Designed system architecture
Implemented gesture recognition logic
Integrated multimedia and system controls
Developed user interface and testing
