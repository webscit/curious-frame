# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Audio module for the Curious Frame project."""
import subprocess
import tempfile

import requests


class Audio:
    """A class to handle audio input and output."""

    def __init__(
        self,
        piper_url: str = "http://127.0.0.1:5000",
        aplay_device: str = "sysdefault",
    ) -> None:
        """Initializes the Audio class.

        Args:
            piper_url: The URL of the piper server.
            aplay_device: The aplay device to use for audio output.
        """
        self.piper_url = piper_url
        self.aplay_device = aplay_device

    def speak(self, text: str) -> None:
        """Speaks the given text.

        Args:
            text: The text to speak.
        """
        response = requests.get(self.piper_url, params={"text": text}, timeout=60)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav.write(response.content)
            temp_wav_path = temp_wav.name

        try:
            subprocess.run(
                ["aplay", "-D", self.aplay_device, temp_wav_path],
                check=True,
                capture_output=True,
                text=True,
            )
        finally:
            # Clean up the temporary file
            import os

            os.remove(temp_wav_path)
