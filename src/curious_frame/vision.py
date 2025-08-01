# SPDX-FileCopyrightText: 2024-present Jetorin <jetorin@example.com>
#
# SPDX-License-Identifier: MIT
"""Vision module for the Curious Frame project."""
import cv2
import numpy as np
from nanoowl.owl_predictor import OwlPredictor
from nanoowl.tree import Tree
from nanoowl.tree_predictor import (
    TreePredictor
)
import PIL.Image

OWL_ENCODER_ENGINE = "/opt/nanoowl/data/owl_image_encoder_patch32.engine"


class Vision:
    """A class to handle vision-related tasks."""

    def __init__(self, threshold: float = 0.1):
        """Initializes the Vision module.

        Args:
            threshold: The confidence threshold for object detection.
        """
        self.predictor = TreePredictor(
            owl_predictor=OwlPredictor(
                image_encoder_engine=OWL_ENCODER_ENGINE,
            )
        )
        self.text = '["a frame"]'
        self.threshold = threshold
        tree = Tree.from_prompt(self.text)
        clip_encodings = self.predictor.encode_clip_text(tree)
        owl_encodings = self.predictor.encode_owl_text(tree)
        self._prompt_data = {
            "tree": tree,
            "clip_text_encodings": clip_encodings,
            "owl_text_encodings": owl_encodings
        }

    def find_frame(self, frame: np.ndarray) -> np.ndarray | None:
        """Finds the frame in the image.

        Args:
            frame: The image to search for the frame in.

        Returns:
            The cropped image of the frame, or None if no frame is found.
        """
        image = _cv2_to_pil(frame)

        output = self.predictor.predict(
            image=image, **self._prompt_data, threshold=self.threshold
        )

        detections = [*output.detections][1:]  # Skip the first detection which is usually the background
        if len(detections) == 0:
            print("No detections found.")
            return None
        else:
            print(f"Found detections: {detections}")
        
        # Find the detection with the largest area
        areas = []
        for detection in filter(lambda d: d.scores[0] > self.threshold, detections):
            box = detection.box
            x_min, y_min, x_max, y_max = [*map(int, box)]
            area = (x_max - x_min) * (y_max - y_min)
            areas.append(area)

        max_idx = int(np.argmax(areas))
        
        # Get the largest bounding box
        x_min, y_min, x_max, y_max = [*map(int, detections[max_idx].box)]

        print(f"Found frame at: {x_min}, {y_min}, {x_max}, {y_max}")
        # Crop the image to the bounding box
        return frame[y_min : y_max, x_min : x_max]

def _cv2_to_pil(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(image)