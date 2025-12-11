# SPDX-FileCopyrightText: 2025-present Frédéric Collonval <frederic.collonval@webscit.com>
#
# SPDX-License-Identifier: MIT
"""Language module for the Curious Frame project."""

import logging

import requests

logger = logging.getLogger(__name__)

GENERATION_OPTIONS = {
    "num_predict": 80,    # Maximum response length
    "temperature": 0.7,   # Creativity (0.0-1.0)
    "top_p": 0.9         # Response diversity
}

class Language:
    """A class to interact with the language model."""

    def __init__(
        self,
        model: str = "hf.co/unsloth/gemma-3n-E2B-it-GGUF:Q4_K_M",
        url: str = "http://127.0.0.1:11434/api/chat",
    ):
        """Initializes the language model.

        Args:
            model: The name of the model to use.
            url: The URL of the Ollama API.
        """
        self.model = model
        self.url = url

    def chat(self, query: str) -> str:
        """Generates a description of the objects from the language model.

        Args:
            query: The query to send asking for the objects to describe.

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
                    You should provide a short, simple description suitable for a child between 2 and 8 years old.
                    Express yourself as a person telling a story to the child. Don't use Markdown format and don't use emojis."""
                },
                {
                    "role": "user",
                    "content": query,
                }
            ],
            "stream": False,
            "keep_alive": -1,
        }

        logger.info(f"Prompt sent: {data}")
        response = requests.post(self.url, json=data)
        response.raise_for_status()
        return response.json().get("message", {}).get("content").strip()

    def translate(self, text: str, language: str) -> str:
        """Translate a text to a given language.

        Args:
            text: The text to translate.
            language: The language to translate to.

        Returns:
            The translated text.
        """
        language = language.capitalize()
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that translates text from English into {language}."
                    "Do not use any special formatting or emojis in your response."
                    f"Provide only the {language} translation",
                },
                {"role": "user", "content": f'Translate the following text: "{text}"'},
            ],
            "stream": False,
            "keep_alive": -1,
        }

        logger.info(f"Translation prompt sent: {data}")
        response = requests.post(self.url, json=data)
        response.raise_for_status()
        return response.json().get("message", {}).get("content").strip()
