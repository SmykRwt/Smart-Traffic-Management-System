"""
Result Parser

Converts YOLO Results into Detection objects.
Supports both:
1. General YOLO model
2. Emergency Vehicle YOLO model
"""

from app.models.bounding_box import BoundingBox
from app.models.detection import Detection
from app.core.config import VEHICLE_CLASSES

class ResultParser:
    def calculate_iou(self, box1, box2):

        x_left = max(box1.x1, box2.x1)
        y_top = max(box1.y1, box2.y1)
        x_right = min(box1.x2, box2.x2)
        y_bottom = min(box1.y2, box2.y2)

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection = (x_right - x_left) * (y_bottom - y_top)

        area1 = (box1.x2 - box1.x1) * (box1.y2 - box1.y1)
        area2 = (box2.x2 - box2.x1) * (box2.y2 - box2.y1)

        union = area1 + area2 - intersection

        return intersection / union


    def remove_duplicate_detections(
        self,
        general_detections,
        emergency_detections,
    ):

        filtered = []

        for general in general_detections:

            duplicate = False

            for emergency in emergency_detections:

                iou = self.calculate_iou(
                    general.bbox,
                    emergency.bbox,
                )

                if iou > 0.50:

                    duplicate = True
                    if emergency.track_id is None and general.track_id is not None:
                        emergency.track_id = general.track_id

                    break

            if not duplicate:
                filtered.append(general)

        filtered.extend(emergency_detections)

        return filtered
    def _parse_single(self, results, filter_classes=None):

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        # Get frame dimensions to perform size filtering
        height, width = result.orig_shape if hasattr(result, "orig_shape") else (720, 1280)
        frame_area = height * width

        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = result.names[class_id]

            if filter_classes is not None:
                if class_name not in filter_classes:
                    continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Calculate box size
            box_width = x2 - x1
            box_height = y2 - y1
            box_area = box_width * box_height

            # Discard detections covering > 30% of the frame or > 80% of width/height (false positives spanning the entire road)
            if box_area > 0.30 * frame_area or box_width > 0.80 * width or box_height > 0.80 * height:
                continue

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

    def parse(self, general_results, emergency_results=None):

        general_detections = self._parse_single(
            general_results,
            VEHICLE_CLASSES,
        )

        emergency_detections = []

        if emergency_results is not None:

            emergency_detections = self._parse_single(
                emergency_results
            )

        detections = self.remove_duplicate_detections(
            general_detections,
            emergency_detections,
        )

        return detections