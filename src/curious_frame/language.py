# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Language module for the Curious Frame project."""

import requests

GENERATION_OPTIONS = {
    "num_predict": 80,    # Maximum response length
    "temperature": 0.7,   # Creativity (0.0-1.0)
    "top_p": 0.9         # Response diversity
}

class Language:
    """A class to interact with the language model."""

    def __init__(
        self, model: str = "unsloth/gemma-3n-E2B-it-GGUF", url: str = "http://localhost:11434/api/chat"
    ):
        """Initializes the language model.

        Args:
            model: The name of the model to use.
            url: The URL of the Ollama API.
        """
        self.model = model
        self.url = url

    def chat(self, objects: str) -> str:
        """Generates a description of the objects from the language model.

        Args:
            objects: The objects to describe.

        Returns:
            The description of the objects.
        """
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are a helpful assistant that describes objects displayed by a child. 
                    The child is curious and asks questions about the objects.
                    You should provide a short, simple description suitable for a child between 2 and 8 years old."""
                },
                {
                    "role": "user",
                    "content": f"Provide a short description of those objects: {objects}.",
                }
            ],
            "stream": True,
            "keep_alive": -1,
        }
        response = requests.post(self.url, json=data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json().get('response', '').strip()
