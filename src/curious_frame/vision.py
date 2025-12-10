# SPDX-FileCopyrightText: 2025-present Frédéric Collonval <frederic.collonval@webscit.com>
#
# SPDX-License-Identifier: MIT
"""Vision module for the Curious Frame project."""

import base64
import json
import logging
from io import BytesIO

import cv2
import numpy as np
import PIL.Image
import requests

logger = logging.getLogger(__name__)


class Vision:
    """A class to handle vision-related tasks."""

    def __init__(
        self,
        model_name: str = "vikhyatk/moondream2",
        revision: str = "2025-06-21",
        url: str = ""
    ):
        """Initializes the Vision module."""
        self.url = url
        self._model_name = model_name
        if url:
            self.model = model_name
        else:
            from transformers import AutoModelForCausalLM, QuantoConfig
            
            quanto_config = QuantoConfig(weights="int8")

            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                revision=revision,
                trust_remote_code=True,
                device_map="auto",
                quantization_config=quanto_config,
            )

        self.query = """List object within the cardboard frame.
Format the response as a comma-separated list of object names, without any additional text or formatting.
If there is no cardboard frame, return _no cardboard frame_."""

    def find_objects(self, frame: np.ndarray) -> str | None:
        """Finds the objects displayed in the cardboard frame within the image.

        Args:
            frame: The image to search for the frame in.

        Returns:
            The objects found in the cardboard frame, or None if no objects are found.
        """
        image = _cv2_to_pil(frame)

        objects = None
        if self.url:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            response = requests.post(self.url, json={"model": self.model, "messages": [{"role": "user", "content": "Is there a French flag in the image? Answer with Yes or No.", "images": [image_b64]}],"stream":False, "keep_alive": -1})
            response.raise_for_status()
            response_content = response.json().get("message", {}).get("content", "").strip().lower()
            found_french_flag = "yes" == response_content
            logger.info("Found a French flag: %s", response_content)
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": self.query
                    },
                    {
                        "role": "user",
                        "content": "Liste uniquement les objets dans le cadre en carton. Réponds en français." if found_french_flag else "List only the objects within the cardboard frame.",
                        "images": [],
                    }
                ],
                "stream": False,
                "keep_alive": -1,
            }
            
            logger.info(f"Prompt sent: {json.dumps(data)}")
            # Add the encoded image after printing the log info
            data["messages"][-1]["images"] = [image_b64]
            response = requests.post(self.url, json=data)
            response.raise_for_status()
            objects = response.json().get("message", {}).get("content").strip()
            if found_french_flag:
                objects += f",French flag"

        else:
            output = self.model.query(image, self.query)

            if output is not None and output.get("answer", ""):
                objects = output["answer"]

        logger.info(f"Found objects using {self._model_name}: {objects}")
        return objects if 'no cardboard frame' not in objects.lower() else None


def _cv2_to_pil(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(image)
