"""
Emergency Vehicle Detector

Identifies emergency vehicles from
the parsed detections.
"""

from app.core.config import EMERGENCY_CLASSES


class EmergencyVehicleDetector:

    def detect(self, detections):

        emergency = []

        for detection in detections:

            if detection.class_name.lower() in EMERGENCY_CLASSES:

                emergency.append(detection)

        return emergency