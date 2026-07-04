import unittest
import time
from unittest.mock import MagicMock

from app.models.bounding_box import BoundingBox
from app.models.detection import Detection
from app.vision.result_parser import ResultParser
from app.analytics.stopped_vehicle_detector import StoppedVehicleDetector
from app.analytics.analytics_engine import AnalyticsEngine
from app.rules.rule_engine import RuleEngine
from app.database.repository import AnalyticsRepository
from app.database.models import Analytics


class TestAIVisionPipeline(unittest.TestCase):

    def test_bounding_box_properties(self):
        bbox = BoundingBox(x1=10, y1=20, x2=110, y2=120)
        self.assertEqual(bbox.width, 100)
        self.assertEqual(bbox.height, 100)
        self.assertEqual(bbox.center, (60, 70))
        self.assertEqual(bbox.area, 10000)

    def test_result_parser_duplicate_removal_and_tracking_inheritance(self):
        parser = ResultParser()

        # General detection of a truck that has tracking ID 14
        general_det = Detection(
            track_id=14,
            class_id=7,
            class_name="truck",
            confidence=0.85,
            bbox=BoundingBox(x1=100, y1=100, x2=200, y2=200)
        )

        # Emergency detection of an ambulance with no tracking ID (comes from detection-only model)
        emergency_det = Detection(
            track_id=None,
            class_id=0,
            class_name="ambulance",
            confidence=0.92,
            bbox=BoundingBox(x1=105, y1=105, x2=195, y2=195)
        )

        # Remove duplicates
        filtered = parser.remove_duplicate_detections([general_det], [emergency_det])

        # We expect:
        # 1. Only 1 detection is kept (the emergency vehicle)
        # 2. It inherits tracking ID 14 from the truck
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].class_name, "ambulance")
        self.assertEqual(filtered[0].track_id, 14)

    def test_stopped_vehicle_detector(self):
        detector = StoppedVehicleDetector()

        # Frame 1 at t=0: Vehicle 5 is at (100, 100)
        det_1 = Detection(
            track_id=5,
            class_id=2,
            class_name="car",
            confidence=0.9,
            bbox=BoundingBox(x1=90, y1=90, x2=110, y2=110) # center is (100, 100)
        )
        stopped_ids = detector.detect([det_1], current_time=0.0)
        self.assertEqual(len(stopped_ids), 0)

        # Frame 2 at t=3.0: Vehicle 5 is still at (100, 100) (not stopped yet, threshold is 6.0s)
        stopped_ids = detector.detect([det_1], current_time=3.0)
        self.assertEqual(len(stopped_ids), 0)

        # Frame 3 at t=7.0: Vehicle 5 is still at (100, 100) (should be stopped!)
        stopped_ids = detector.detect([det_1], current_time=7.0)
        self.assertIn(5, stopped_ids)

        # Frame 4 at t=8.0: Vehicle 5 moves to (500, 500)
        det_moved = Detection(
            track_id=5,
            class_id=2,
            class_name="car",
            confidence=0.9,
            bbox=BoundingBox(x1=490, y1=490, x2=510, y2=510) # center is (500, 500)
        )
        stopped_ids = detector.detect([det_moved], current_time=8.0)
        self.assertEqual(len(stopped_ids), 0) # No longer stopped

    def test_analytics_and_rule_engine(self):
        analytics_engine = AnalyticsEngine()
        rule_engine = RuleEngine()

        # Simulate heavy congestion
        detections = []
        for i in range(15):
            detections.append(
                Detection(
                    track_id=i,
                    class_id=2,
                    class_name="car",
                    confidence=0.8,
                    bbox=BoundingBox(x1=0, y1=0, x2=10, y2=10)
                )
            )

        analytics = analytics_engine.analyze(detections, current_time=1.0)
        self.assertEqual(analytics.current_vehicle_count, 15)
        self.assertEqual(analytics.congestion_level, "HEAVY")

        # Evaluate rules
        matched_rules = rule_engine.evaluate(analytics)
        matched_names = [rule.name for rule in matched_rules]
        self.assertIn("Heavy Traffic", matched_names)

    def test_database_repository(self):
        repository = AnalyticsRepository()

        # Create a mock analytics result
        mock_analytics = MagicMock()
        mock_analytics.current_vehicle_count = 8
        mock_analytics.unique_vehicle_count = 12
        mock_analytics.traffic_density = "MEDIUM"
        mock_analytics.congestion_level = "MODERATE"

        # Save to database
        try:
            repository.save(mock_analytics)
            success = True
        except Exception as e:
            success = False
            print(f"Database save failed: {e}")

        self.assertTrue(success)

        # Retrieve history
        if success:
            history = repository.get_history(limit=5)
            self.assertGreater(len(history), 0)
            last_record = history[-1]
            self.assertEqual(last_record.current_vehicle_count, 8)
            self.assertEqual(last_record.unique_vehicle_count, 12)
            self.assertEqual(last_record.traffic_density, "MEDIUM")
            self.assertEqual(last_record.congestion_level, "MODERATE")


if __name__ == "__main__":
    unittest.main()
