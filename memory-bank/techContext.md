# Tech Context

This document details the technologies, development setup, and technical constraints for the project.

## Technologies

- Python for the application
- opencv for interacting with the camera

## Development Setup

- The project should be a valid python package
- The project should use ruff as a linter/formatter
- All code should be typed and documented using docstring with Google syntax.

## Technical Constraints

- The application is executed on a Jetson Orin Nano 8Gb
- Keep usage resource as small as possible
- The camera is a Raspberry Pi Camera v2 with resolution of 1280x720 and 30 FPS on /dev/video0
- The sound speaker and microphone are provided by a Jabra Speak2 55
