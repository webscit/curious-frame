# SPDX-FileCopyrightText: 2025-present Frédéric Collonval <frederic.collonval@webscit.com>
#
# SPDX-License-Identifier: MIT
"""Audio module for the Curious Frame project."""
import hashlib
import os
import subprocess

import requests

from src.curious_frame.language import Language


class Audio:
    """A class to handle audio input and output."""

    def __init__(
        self,
        piper_url: str = "http://127.0.0.1:5000",
        aplay_device: str = "sysdefault",
        language: str = "en",
        language_model: Language | None = None,
    ) -> None:
        """Initializes the Audio class.

        Args:
            piper_url: The URL of the piper server.
            aplay_device: The aplay device to use for audio output.
            language: The language to use for audio output.
            language_model: The language model to use for translation.
        """
        self.piper_url = piper_url
        self.aplay_device = aplay_device
        self.language = language
        self.language_model = language_model
        self.cache_dir = "audio_cache"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def set_language(self, language: str) -> None:
        """Set the language for audio output.

        Args:
            language: The language to set.
        """
        self.language = language

    def speak(self, text: str, language: str | None = None, skip_translation: bool = False) -> None:
        """Speaks the given text, using a cache to avoid regenerating audio.

        Args:
            text: The text to speak.
            language: The language to use for the audio output.
                If None, the default language is used.
        """
        lang = language or self.language
        is_french = lang == "fr"
        # Generate a unique filename from the hash of the text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if is_french:
            text_hash += "_fr"
        cached_audio_path = os.path.join(self.cache_dir, f"{text_hash}.wav")

        if not os.path.exists(cached_audio_path):
            to_speak = text
            if is_french and not skip_translation:
                if self.language_model is None:
                    raise ValueError(
                        "Language model is required for French translation."
                    )
                to_speak = self.language_model.translate(text, "french")

            data = {"text": to_speak}
            if is_french:
                data["voice"] = "fr_FR-upmc-medium"
                data["speaker_id"] = 0

            response = requests.post(self.piper_url, json=data, timeout=60)
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
