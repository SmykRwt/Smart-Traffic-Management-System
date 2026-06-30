"""
Result Parser

Converts YOLO Results into Detection objects.
"""

from app.models.bounding_box import BoundingBox
from app.models.detection import Detection
from app.core.config import VEHICLE_CLASSES


class ResultParser:

    def parse(self, results):

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = result.names[class_id]

            # Ignore non-vehicle classes
            if class_name not in VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            track_id = None

            if box.id is not None:
                track_id = int(box.id.item())

            bbox = BoundingBox(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
            )

            detections.append(
                Detection(
                    track_id=track_id,
                    class_id=class_id,
                    class_name=class_name,
                    confidence=confidence,
                    bbox=bbox,
                )
            )

        return detections