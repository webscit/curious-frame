# Active Context

This document tracks the current focus of development, including recent changes, next steps, and active considerations.

## Current Focus

The current focus is on refining the vision module and preparing for the integration of the language model. With the camera and basic frame detection now functional, the next priority is to improve the accuracy of the frame detection and extract the action card and image from within the frame.

## Recent Changes

- **Camera Integration**: Successfully configured the GStreamer pipeline for a USB camera, resolving initial camera access issues. The camera now correctly captures frames.
- **Vision Implementation**: Implemented a basic version of the `find_frame` method in `vision.py` using OpenCV's contour detection to find and crop the cardboard frame from the camera feed.
- **Main Loop Integration**: Updated `main.py` to use the `Vision` module to process frames from the camera.
- **Initial Tests**: Created `tests/test_camera.py` with a basic unit test to ensure the `Camera` class can be initialized.

## Next Steps

The immediate next steps are:

1.  **Refine Frame Detection**: Improve the `find_frame` method in `vision.py` to be more robust. This may involve using more advanced techniques like shape approximation to ensure the detected contour is a rectangle.
2.  **Extract Action Card and Image**: Implement logic to identify and extract the two regions of interest from within the detected frame: the action card and the main image.
3.  **Integrate Language Model**: Begin implementing the `language.py` module to take the extracted image and action card as input and generate a prompt for the Gemma3n model.
4.  **Develop Vision Tests**: Create `tests/test_vision.py` to test the frame and sub-region detection logic.
