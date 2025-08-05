# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Main module for the Curious Frame project."""

from curious_frame.audio import Audio
from curious_frame.camera import Camera
from curious_frame.language import Language
from curious_frame.vision import Vision


def main() -> None:
    """The main function for the Curious Frame project."""
    camera = Camera()
    vision = Vision()
    language = Language()
    audio = Audio()

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        objects = vision.find_objects(frame)
        if objects is not None:
            description = language.chat(objects)
            print(f"Description: {description}")
            audio.speak(description)
        else:
            print("No objects found.")

        break
    camera.release()


if __name__ == "__main__":
    main()
