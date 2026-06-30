from dataclasses import dataclass

from app.models.bounding_box import BoundingBox


@dataclass
class Detection:

    track_id: int | None

    class_id: int

    class_name: str

    confidence: float

    bbox: BoundingBox