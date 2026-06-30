"""
Vision Engine

Central AI service of the platform.

Responsibilities:
1. Load the AI model once.
2. Perform object detection.
3. Perform multi-object tracking.
4. Expose a clean interface to the application.

This module is the only one that directly interacts
with Ultralytics YOLO.
"""

from ultralytics import YOLO

from app.core.config import (
    MODEL_NAME,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
)

from app.core.logger import logger


class VisionEngine:

    def __init__(self):

        logger.info("Loading Vision Engine...")

        self.model = YOLO(MODEL_NAME)

        logger.info("Vision Engine Ready.")

    def detect(self, frame):

        return self.model(
            frame,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False,
        )

    def track(self, frame):

        return self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False,
        )

    def predict(self, frame, tracking=True):

        if tracking:
            return self.track(frame)

        return self.detect(frame)