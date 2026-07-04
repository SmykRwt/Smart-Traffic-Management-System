from ultralytics import YOLO

from app.core.config import (
    GENERAL_MODEL,
    EMERGENCY_MODEL,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
)

from app.core.logger import logger


class VisionEngine:

    def __init__(self):

        logger.info("Loading Vision Engine...")

        logger.info("Loading General Detection Model...")
        self.general_model = YOLO(GENERAL_MODEL)

        logger.info("Loading Emergency Vehicle Model...")
        self.emergency_model = YOLO(EMERGENCY_MODEL)

        logger.info("Vision Engine Ready.")

    # -----------------------------
    # General Detection
    # -----------------------------

    def detect(self, frame, conf=None):

        if conf is None:
            conf = CONFIDENCE_THRESHOLD

        return self.general_model(
            frame,
            conf=conf,
            iou=IOU_THRESHOLD,
            verbose=False,
        )

    def track(self, frame, conf=None):

        if conf is None:
            conf = CONFIDENCE_THRESHOLD

        return self.general_model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=conf,
            iou=IOU_THRESHOLD,
            verbose=False,
        )

    def predict(self, frame, tracking=True, conf=None):

        if tracking:
            return self.track(frame, conf=conf)

        return self.detect(frame, conf=conf)

    # -----------------------------
    # Emergency Vehicle Detection
    # -----------------------------

    def detect_emergency(self, frame, conf=None):

        if conf is None:
            conf = CONFIDENCE_THRESHOLD

        return self.emergency_model(
            frame,
            conf=conf,
            iou=IOU_THRESHOLD,
            verbose=False,
        )