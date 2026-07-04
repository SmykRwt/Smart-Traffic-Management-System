from collections import defaultdict

from app.analytics.analytics_result import AnalyticsResult
from app.analytics.metrics.traffic_density import (
    TrafficDensityCalculator,
)
from app.analytics.metrics.fps_counter import FPSCounter
from app.analytics.metrics.congestion import (
    CongestionCalculator,
)
from app.analytics.stopped_vehicle_detector import (
    StoppedVehicleDetector,
)
from app.analytics.emergency_vehicle_detection import (
    EmergencyVehicleDetector,
)

class AnalyticsEngine:

    def __init__(self):

        self.unique_track_ids = set()
        self.fps_counter = FPSCounter()
        self.traffic_density = TrafficDensityCalculator()
        self.congestion = CongestionCalculator()
        self.stopped_detector = (
            StoppedVehicleDetector()
        )
        self.emergency_detector = EmergencyVehicleDetector()

    def analyze(self, detections, current_time=None):

        vehicle_count = defaultdict(int)
        stopped_ids = self.stopped_detector.detect(
            detections,
            current_time=current_time,
        )
        emergency = self.emergency_detector.detect(
            detections
        )

        for detection in detections:

            vehicle_count[detection.class_name] += 1

            if detection.track_id is not None:
                self.unique_track_ids.add(
                    detection.track_id
                )

        total_objects = len(detections)

        density = self.traffic_density.calculate(
            total_objects
        )

        congestion = self.congestion.calculate(
            total_objects
        )
        fps = self.fps_counter.update()

        return AnalyticsResult(

            fps=fps,

            current_vehicle_count=total_objects,

            unique_vehicle_count=len(
                self.unique_track_ids
            ),

            vehicle_count=dict(vehicle_count),

            traffic_density=density,

            congestion_level=congestion,

            stopped_vehicle_ids=stopped_ids,

            emergency_vehicles=emergency,

        )