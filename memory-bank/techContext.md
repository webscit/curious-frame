# Tech Context

This document details the technologies, development setup, and technical constraints for the project.

## Technologies

- Python for the application
- opencv for interacting with the camera
- use pytest for python unittest
- use [moondream2 VLM](https://github.com/vikhyat/moondream) to list the object within the cardboard frame
- use gemma3n E2B as LLM model as brain
- Piper will be used to speak to the child

## Development Setup

- The project should be a valid python package
- The project should use ruff as a linter/formatter
- All code should be typed and documented using docstring with Google syntax.

## Technical Constraints

- The application is executed on a Jetson Orin Nano 8Gb
- Keep usage resource as small as possible
- The camera is a USB Camera with resolution of 1280x720 and 15 FPS on /dev/video0
- The sound speaker and microphone are provided by a Jabra Speak2 55
- Gemma3n will be executed using ollama as this is the only way to make it run on the Jetson Orin Nano
- Piper will be executed in a docker and interact with through a HTTP server
