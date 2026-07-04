import math
import time

from app.core.config import (
    STOPPED_DISTANCE_THRESHOLD,
    STOPPED_TIME_THRESHOLD,
)


class StoppedVehicleDetector:

    def __init__(self):

        self.history = {}

    def detect(self, detections, current_time=None):

        if current_time is None:
            current_time = time.time()

        stopped_ids = []

        active_tracks = set()

        for detection in detections:

            if detection.track_id is None:
                continue

            track_id = detection.track_id

            active_tracks.add(track_id)

            x, y = detection.bbox.center

            if track_id not in self.history:

                self.history[track_id] = {

                    "position": (x, y),
                    "last_move": current_time,

                }

                continue

            last_x, last_y = self.history[track_id]["position"]

            distance = math.sqrt(

                (x - last_x) ** 2
                +
                (y - last_y) ** 2

            )

            if distance > STOPPED_DISTANCE_THRESHOLD:

                self.history[track_id]["position"] = (
                    x,
                    y,
                )

                self.history[track_id]["last_move"] = current_time

            else:

                stopped_time = (
                    current_time
                    - self.history[track_id]["last_move"]
                )

                if stopped_time >= STOPPED_TIME_THRESHOLD:

                    stopped_ids.append(track_id)

        inactive = set(self.history.keys()) - active_tracks

        for track_id in inactive:

            del self.history[track_id]

        return stopped_ids