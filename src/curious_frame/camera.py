# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Camera module for the Curious Frame project."""
import cv2
import numpy as np


class Camera:
    """A class to interact with the camera."""

    def __init__(self, camera_id: int = 0, width: int = 1280, height: int = 720, fps=30) -> None:
        """Initializes the camera.

        Args:
            camera_id: The ID of the camera to use.
            width: The width of the camera frame.
            height: The height of the camera frame.
        """
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

    def get_frame(self) -> np.ndarray | None:
        """Gets a frame from the camera.

        Returns:
            The frame from the camera, or None if the frame could not be read.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self) -> None:
        """Releases the camera."""
        self.cap.release()
