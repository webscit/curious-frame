# Active Context

This document tracks the current focus of development, including recent changes, next steps, and active considerations.

## Current Focus

The current focus is on internationalization, adding support for French language output.

## Recent Changes

- **French Language Support**: Implemented internationalization to handle French language output.
  - The application now detects the presence of a "french flag" to switch the language.
  - `language.py` was updated to include a `translate` method.
  - `audio.py` was updated to support French TTS and to cache translated audio.
  - `main.py` was updated to orchestrate the language switching.
- **Audio Caching**: Implemented a caching mechanism in `audio.py` to store generated audio files and avoid redundant calls to the TTS server. This improves performance and reduces resource usage.
- **Intermediate Audio Feedback**: Added audio cues to `main.py` to inform the user about the application's progress, such as when it's looking for objects and when it has found them.

## Next Steps

The immediate next steps are:

1.  **Refine Frame Detection**: Improve the `find_frame` method in `vision.py` to be more robust. This may involve using more advanced techniques like shape approximation to ensure the detected contour is a rectangle.
2.  **Extract Action Card and Image**: Implement logic to identify and extract the two regions of interest from within the detected frame: the action card and the main image.
3.  **Develop Vision Tests**: Create `tests/test_vision.py` to test the frame and sub-region detection logic.
4.  **Add Audio to `.gitignore`**: Add `audio_cache/` to the `.gitignore` file to avoid committing cached audio files to the repository.
