# SPDX-FileCopyrightText: 2025-present Frédéric Collonval <frederic.collonval@webscit.com>
#
# SPDX-License-Identifier: MIT
"""Vision module for the Curious Frame project."""

import cv2
import numpy as np
import PIL.Image
from transformers import AutoModelForCausalLM, QuantoConfig


class Vision:
    """A class to handle vision-related tasks."""

    def __init__(
        self, model_name: str = "vikhyatk/moondream2", revision: str = "2025-06-21"
    ):
        """Initializes the Vision module."""
        quanto_config = QuantoConfig(weights="int8")

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            revision=revision,
            trust_remote_code=True,
            device_map="auto",
            quantization_config=quanto_config,
        )
        self.query = "List object within the cardboard frame.\nFormat the response as a comma-separated list of objects, without any additional text or formatting."

    def find_objects(self, frame: np.ndarray) -> str | None:
        """Finds the objects displayed in the cardboard frame within the image.

        Args:
            frame: The image to search for the frame in.

        Returns:
            The objects found in the cardboard frame, or None if no objects are found.
        """
        image = _cv2_to_pil(frame)

        output = self.model.query(image, self.query)

        if output is None or not output.get("answer", ""):
            return None

        print(f"Found objects: {output['answer']}")
        return output["answer"]


def _cv2_to_pil(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(image)
