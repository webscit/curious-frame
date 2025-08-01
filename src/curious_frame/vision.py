# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Vision module for the Curious Frame project."""
import cv2
import numpy as np


class Vision:
    """A class to handle vision-related tasks."""

    def find_frame(self, frame: np.ndarray) -> np.ndarray | None:
        """Finds the cardboard frame in the image.

        Args:
            frame: The image to search for the frame in.

        Returns:
            The cropped image of the frame, or None if no frame is found.
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Use Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour
        if not contours:
            return None

        largest_contour = max(contours, key=cv2.contourArea)

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Crop the image to the bounding box
        cropped_frame = frame[y : y + h, x : x + w]

        return cropped_frame
