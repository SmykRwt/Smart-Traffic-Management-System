import os
import cv2

from app.core.logger import logger

from app.utils.visualization import Visualizer
from app.vision.vision_engine import VisionEngine
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

    def process_video_stream(self, video_path, conf=None):

        logger.info(f"Opening video: {video_path}")

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise Exception("Unable to open video.")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0

        frame_index = 0

        try:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                general_results = self.vision_engine.predict(
                    frame,
                    tracking=True,
                    conf=conf
                )

                emergency_results = self.vision_engine.detect_emergency(
                    frame,
                    conf=conf
                )

                detections = self.parser.parse(
                    general_results,
                    emergency_results
                )

                current_time = frame_index / fps
                analytics = self.analytics.analyze(detections, current_time=current_time)

                if self.scheduler.should_save():
                    self.repository.save(analytics)

                matched_rules = self.rule_engine.evaluate(
                    analytics
                )

                events = self.event_engine.generate(
                    matched_rules
                )

                # Draw detections (bounding boxes) and HUD stats onto the frame
                annotated_frame = frame.copy()
                annotated_frame = self.visualizer.draw(annotated_frame, detections)
                annotated_frame = self.HUD.draw(
                    annotated_frame,
                    analytics,
                    events,
                )

                frame_index += 1

                yield annotated_frame, analytics, events, detections, None

        finally:
            cap.release()
            logger.info("Video processing completed.")

    def process_video(self, video_path, conf=None):
        latest_summary = {}
        for frame, analytics, events, detections, _ in self.process_video_stream(video_path, conf=conf):
            latest_summary = {
                "analytics": analytics,
                "events": [str(event) for event in events],
                "detections": len(detections),
            }
        return None, latest_summary