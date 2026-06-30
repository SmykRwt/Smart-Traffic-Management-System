"""
Tracking Engine

Responsibilities
----------------
1. Run multi-object tracking.
2. Assign unique IDs to detected objects.
3. Return tracking results.

No visualization.
No analytics.
No event detection.
"""

from ultralytics import YOLO

from app.core.config import (
    MODEL_NAME,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
)

from app.core.logger import logger


class Tracker:

    def __init__(self):

        logger.info("Loading YOLO model for tracking...")

        self.model = YOLO(MODEL_NAME)

        logger.info("Tracking model initialized.")

    def track(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            tracker="bytetrack.yaml",
            verbose=False,
        )

        return results