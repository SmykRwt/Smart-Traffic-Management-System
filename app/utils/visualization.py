"""
Visualization Module

Responsible for drawing detections on frames.

This module DOES NOT perform AI inference.
It only visualizes parsed Detection objects.
"""

import cv2

from app.core.colors import CLASS_COLORS, DEFAULT_COLOR
from app.core.config import (
    FONT_SCALE,
    FONT_THICKNESS,
    BOX_THICKNESS,
)


class Visualizer:

    def __init__(self):
        pass

    def draw(self, frame, detections):
        """
        Draw all detections on a frame.

        Args:
            frame: OpenCV image
            detections: List[Detection]

        Returns:
            Annotated frame
        """

        for detection in detections:

            color = CLASS_COLORS.get(
                detection.class_name,
                DEFAULT_COLOR,
            )

            if detection.track_id is None:
                label = (
                    f"{detection.class_name} "
                    f"{detection.confidence:.2f}"
                )
            else:
                label = (
                    f"ID {detection.track_id} | "
                    f"{detection.class_name} "
                    f"{detection.confidence:.2f}"
                )

            # Draw bounding box
            cv2.rectangle(
                frame,
                (detection.bbox.x1, detection.bbox.y1),
                (detection.bbox.x2, detection.bbox.y2),
                color,
                BOX_THICKNESS,
            )

            # Draw label
            cv2.putText(
                frame,
                label,
                (detection.bbox.x1, detection.bbox.y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE,
                color,
                FONT_THICKNESS,
            )

        return frame