"""
Congestion Detection Metric
"""


class CongestionCalculator:

    def __init__(
        self,
        low_threshold=5,
        medium_threshold=12,
        high_threshold=20,
    ):

        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold

    def calculate(self, vehicle_count: int):

        if vehicle_count <= self.low_threshold:
            return "FREE FLOW"

        elif vehicle_count <= self.medium_threshold:
            return "MODERATE"

        elif vehicle_count <= self.high_threshold:
            return "HEAVY"

        return "SEVERE"