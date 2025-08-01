# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Main module for the Curious Frame project."""
import cv2

from curious_frame.camera import Camera


def main() -> None:
    """The main function for the Curious Frame project."""
    camera = Camera()
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        # cv2.imshow("Curious Frame", frame)
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        output_filename = "output_frame.jpg"
        cv2.imwrite(output_filename, frame)
        print(f"Frame saved as {output_filename}")
        break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
