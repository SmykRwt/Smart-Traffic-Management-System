from dataclasses import dataclass


@dataclass
class AnalyticsResult:

    fps: float

    current_vehicle_count: int

    unique_vehicle_count: int

    vehicle_count: dict[str, int]

    traffic_density: str

    congestion_level: str