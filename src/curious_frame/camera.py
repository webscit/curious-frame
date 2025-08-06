# SPDX-FileCopyrightText: 2025-present Frédéric Collonval <frederic.collonval@webscit.com>
#
# SPDX-License-Identifier: MIT
"""Camera module for the Curious Frame project."""
import cv2
import numpy as np


class Camera:
    """A class to interact with the camera."""

    def __init__(self, camera_id: int = 0, width: int = 1280, height: int = 720, fps=15) -> None:
        """Initializes the camera.

        Args:
            camera_id: The ID of the camera to use.
            width: The width of the camera frame.
            height: The height of the camera frame.
        """
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None

    def get_frame(self) -> np.ndarray | None:
        """Gets a frame from the camera.

        Returns:
            The frame from the camera, or None if the frame could not be read.
        """
        self.cap = cv2.VideoCapture(
            self._gstreamer_pipeline(self.camera_id, self.width, self.height, self.fps),
            cv2.CAP_GSTREAMER,
        )
        if not self.cap.isOpened():
            return None

        try:
            ret, frame = self.cap.read()
        finally:
            self.release()

        if not ret:
            return None
        return frame

    def release(self) -> None:
        """Releases the camera."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def save_frame(self, path: str, frame: np.ndarray) -> None:
        """Saves a frame to a file.

        Args:
            path: The path to save the frame to.
            frame: The frame to save.
        """
        cv2.imwrite(path, frame)

    def _gstreamer_pipeline(
        self,
        camera_id: int = 0,
        capture_width: int = 1920,
        capture_height: int = 1080,
        framerate: int = 15,
    ) -> str:
        """Create a GStreamer pipeline for the camera.

        Args:
            camera_id: The ID of the camera to use.
            capture_width: The width of the camera frame.
            capture_height: The height of the camera frame.
            framerate: The framerate of the camera.

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
