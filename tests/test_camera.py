# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Tests for the camera module."""
import unittest
from unittest.mock import MagicMock, patch

from curious_frame.camera import Camera


class TestCamera(unittest.TestCase):
    """Tests for the Camera class."""

    @patch("cv2.VideoCapture")
    def test_camera_initialization(self, mock_video_capture: MagicMock) -> None:
        """Test that the camera can be initialized."""
        # Arrange
        mock_capture_instance = MagicMock()
        mock_video_capture.return_value = mock_capture_instance

        # Act
        camera = Camera()

        # Assert
        self.assertIsNotNone(camera)
        mock_video_capture.assert_called_once()


if __name__ == "__main__":
    unittest.main()
