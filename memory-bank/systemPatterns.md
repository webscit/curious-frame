# System Patterns

This document outlines the system architecture, key technical decisions, and design patterns that guide the project's implementation.

## System Architecture

The application is designed with a modular architecture to separate core functionalities. This approach promotes code reusability, simplifies testing, and makes the system easier to maintain and extend. The key modules are:

- **`camera.py`**: Manages the video stream from the Raspberry Pi camera using OpenCV. It handles camera initialization, frame capture, and resource release.
- **`vision.py`**: Responsible for all computer vision tasks. This includes analyzing video frames to detect the cardboard frame, extracting the action card, and identifying the image within the frame.
- **`language.py`**: Interfaces with the Gemma3n language model via Ollama. It takes the processed information from the vision module as input, constructs a prompt, and retrieves the model's response.
- **`audio.py`**: Handles all audio-related functionalities. This includes text-to-speech (TTS) to voice the model's responses and will be extended to include speech-to-text (STT) for future user interaction.
- **`main.py`**: The main entry point of the application. It orchestrates the workflow by initializing all modules and managing the flow of data between them—from capturing a frame to speaking the response.

## Key Technical Decisions

*To be defined.*

## Design Patterns

*To be defined.*
