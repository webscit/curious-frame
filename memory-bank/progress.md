# Progress

This document tracks the project's status, including what works, what's left to build, and any known issues.

- **Project Scaffolding**: A complete Python package structure has been created with `pyproject.toml`, a `src` directory containing the main package, and a `tests` directory.
- **Modular Structure**: The core modules (`camera`, `audio`, `language`, `vision`, `main`) have been created with initial class definitions and placeholder logic.
- **Camera Module**: The `camera.py` module is implemented with a `Camera` class that correctly initializes a USB camera on a Jetson device using a GStreamer pipeline.
- **Basic Vision**: The `vision.py` module can perform basic contour detection to find and crop a frame from the camera feed.
- **Main Application Loop**: The `main.py` script successfully integrates the camera and vision modules to capture, process, and save a frame.
- **Initial Tests**: A basic test suite has been started with `tests/test_camera.py`.
- **Documentation**: The memory bank is up-to-date with the latest progress and technical decisions.

## What Works

- **Language Model Integration**: The `language.py` module is now integrated with the main application loop. It can take a cropped image, send it to the Gemma3n model, and receive a textual description.
- **Audio Output**: The `audio.py` module is now implemented with a text-to-speech engine to voice the model's responses. The audio module is integrated in the main application loop.

## What's Left to Build

- **Vision Processing**: The `vision.py` module needs to be implemented to detect the cardboard frame and extract the relevant image and action card.
- **Testing**: A comprehensive test suite needs to be developed to ensure the reliability of all modules.

## Known Issues

*To be defined.*
