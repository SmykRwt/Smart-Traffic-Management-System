"""
Traffic Density Metric
"""


class TrafficDensityCalculator:

    def __init__(
        self,
        low_threshold=5,
        medium_threshold=14,
    ):
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold

    def calculate(self, total_vehicles: int) -> str:

        if total_vehicles <= self.low_threshold:
            return "LOW"

        elif total_vehicles <= self.medium_threshold:
            return "MEDIUM"

        return "HIGH"