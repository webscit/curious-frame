# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Audio module for the Curious Frame project."""


class Audio:
    """A class to handle audio input and output."""

    def speak(self, text: str) -> None:
        """Speaks the given text.

        Args:
            text: The text to speak.
        """
        print(f"Speaking: {text}")
