# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Main module for the Curious Frame project."""
import csv
from datetime import datetime
from pathlib import Path

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

    # Create a directory to store the captures
    capture_dir = Path.home() / "curious_frame_captures"
    capture_dir.mkdir(parents=True, exist_ok=True)
    csv_path = capture_dir / "captures.csv"

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        # Save the image first
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = capture_dir / f"{timestamp}.jpg"
        camera.save_frame(str(image_path), frame)

        objects = None
        description = None
        try:
            objects = vision.find_objects(frame)
            if objects is not None:
                description = language.chat(objects)
                print(f"Description: {description}")
                audio.speak(description)
            else:
                print("No objects found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            description = f"Error: {e}"

        # Always store the information in the CSV file
        with open(csv_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    str(image_path),
                    objects if objects else "N/A",
                    description if description else "N/A",
                ]
            )

        break
    camera.release()


if __name__ == "__main__":
    main()
