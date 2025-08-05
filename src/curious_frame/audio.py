# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Audio module for the Curious Frame project."""
import hashlib
import os
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
        self.cache_dir = "audio_cache"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def speak(self, text: str) -> None:
        """Speaks the given text, using a cache to avoid regenerating audio.

        Args:
            text: The text to speak.
        """
        # Generate a unique filename from the hash of the text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        cached_audio_path = os.path.join(self.cache_dir, f"{text_hash}.wav")

        if not os.path.exists(cached_audio_path):
            response = requests.get(self.piper_url, params={"text": text}, timeout=60)
            response.raise_for_status()
            with open(cached_audio_path, "wb") as f:
                f.write(response.content)

        try:
            subprocess.run(
                ["aplay", "-D", self.aplay_device, cached_audio_path],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio: {e.stderr}")
            # Clean up the cached file if playback fails
            if os.path.exists(cached_audio_path):
                os.remove(cached_audio_path)
