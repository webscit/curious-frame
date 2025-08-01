# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Main module for the Curious Frame project."""
import cv2

from curious_frame.camera import Camera
from curious_frame.vision import Vision


def main() -> None:
    """The main function for the Curious Frame project."""
    camera = Camera()
    vision = Vision()
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        cropped_frame = vision.find_frame(frame)
        if cropped_frame is not None:
            output_filename = "output_frame.jpg"
            cv2.imwrite(output_filename, cropped_frame)
            print(f"Frame saved as {output_filename}")
        else:
            print("No frame found.")

        break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
