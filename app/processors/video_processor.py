"""
Video Processing Engine

Responsibilities:
- Open video
- Read frames
- Send frame to detector
- Send results to visualizer
- Display output

No AI logic.
No analytics.
No tracking.
"""

import cv2

from app.core.config import (
    VIDEO_PATH,
    WINDOW_NAME,
)

from app.core.logger import logger
from app.utils.visualization import Visualizer
from app.vision.vision_engine import VisionEngine
from app.tracking.tracker import Tracker
from app.vision.result_parser import ResultParser
from app.analytics.analytics_engine import AnalyticsEngine
from app.utils.HUD import HUD
from app.events.event_engine import EventEngine
from app.rules.rule_engine import RuleEngine
from app.database.repository import AnalyticsRepository
from app.database.analytics_scheduler import AnalyticsScheduler

class VideoProcessor:

    def __init__(self):
        self.repository = AnalyticsRepository()
        self.event_engine = EventEngine()
        self.vision_engine = VisionEngine()
        self.visualizer = Visualizer()
        self.parser = ResultParser()
        self.analytics = AnalyticsEngine()
        self.HUD = HUD()
        self.rule_engine = RuleEngine()
        self.scheduler = AnalyticsScheduler(interval=5)


    def process_video(self):

        logger.info(f"Opening video: {VIDEO_PATH}")

        cap = cv2.VideoCapture(str(VIDEO_PATH))

        if not cap.isOpened():
            logger.error("Unable to open video.")
            return

        logger.info("Video started successfully.")

        while True:

            success, frame = cap.read()

            if not success:
                logger.info("End of video reached.")
                break

            # Run Detection
            results = self.vision_engine.predict(
                frame,
                tracking=True
            )

            detections = self.parser.parse(results)
            analytics = self.analytics.analyze(detections)
            if self.scheduler.should_save():
                self.repository.save(analytics)
            matched_rules = self.rule_engine.evaluate(
                analytics
            )

            events = self.event_engine.generate(
                matched_rules
            )
            frame = self.visualizer.draw(
                frame,
                detections
            )
            frame = self.HUD.draw(
                frame,
                analytics,
                events,
            )
            # Display
            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1)

            if key == ord("q"):
                logger.info("User terminated the application.")
                break

        cap.release()

        cv2.destroyAllWindows()

        logger.info("Resources released.")