# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Language module for the Curious Frame project."""
import ollama


class Language:
    """A class to interact with the language model."""

    def __init__(self, model: str = "gemma3n:e2b"):
        """Initializes the language model.

        Args:
            model: The name of the model to use.
        """
        self.model = model

    def get_response(self, prompt: str) -> str:
        """Gets a response from the language model.

        Args:
            prompt: The prompt to send to the model.

        Returns:
            The response from the model.
        """
        response = ollama.chat(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
