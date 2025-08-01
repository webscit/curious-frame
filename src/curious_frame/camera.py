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
        self.cap = cv2.VideoCapture(self._gstreamer_pipeline(camera_id, width, height, fps), cv2.CAP_GSTREAMER)

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

    def _gstreamer_pipeline(
        self,
        camera_id: int = 0,
        capture_width: int = 1280,
        capture_height: int = 720,
        framerate: int = 30,
        flip_method: int = 0,
    ) -> str:
        """Create a GStreamer pipeline for the camera.

        Args:
            camera_id: The ID of the camera to use.
            capture_width: The width of the camera frame.
            capture_height: The height of the camera frame.
            framerate: The framerate of the camera.
            flip_method: The flip method to use.

        Returns:
            The GStreamer pipeline string.
        """
        return (
            f"v4l2src device=/dev/video{camera_id} ! "
            f"image/jpeg, width=(int){capture_width}, height=(int){capture_height}, framerate=(fraction){framerate}/1 ! "
            "nvjpegdec ! "
            "video/x-raw ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
        )
