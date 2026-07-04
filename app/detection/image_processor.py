"""
Image Processor

Processes a single traffic image through the complete
Smart Traffic Management pipeline.
"""

import cv2
import os

from app.vision.vision_engine import VisionEngine
from app.vision.result_parser import ResultParser

from app.analytics.analytics_engine import AnalyticsEngine
from app.rules.rule_engine import RuleEngine
from app.events.event_engine import EventEngine

from app.utils.visualization import Visualizer


class ImageProcessor:

    def __init__(self):

        self.vision_engine = VisionEngine()

        self.result_parser = ResultParser()

        self.analytics = AnalyticsEngine()

        self.rule_engine = RuleEngine()

        self.event_engine = EventEngine()

        self.visualizer = Visualizer()

    def process_image(self, image_path, conf=None):

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Unable to load image: {image_path}"
            )

        # -------------------------
        # General Vehicle Detection
        # -------------------------

        general_results = self.vision_engine.predict(
            image,
            tracking=False,
            conf=conf,
        )

        # -------------------------
        # Emergency Vehicle Detection
        # -------------------------

        emergency_results = self.vision_engine.detect_emergency(
            image,
            conf=conf,
        )

        # -------------------------
        # Merge both detections
        # -------------------------

        detections = self.result_parser.parse(
            general_results,
            emergency_results,
        )

        # -------------------------
        # Analytics
        # -------------------------

        analytics = self.analytics.analyze(
            detections
        )

        matched_rules = self.rule_engine.evaluate(
            analytics
        )

        events = self.event_engine.generate(
            matched_rules
        )

        # -------------------------
        # Draw Result
        # -------------------------

        output = self.visualizer.draw(
            image,
            detections,
        )

        summary = {

            "analytics": analytics,

            "events": [str(event) for event in events],

            "detections": len(detections),

        }

        return output, summary