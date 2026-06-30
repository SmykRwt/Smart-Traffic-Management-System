import time


class FPSCounter:

    def __init__(self):

        self.previous_time = time.perf_counter()

        self.fps = 0.0

    def update(self):

        current_time = time.perf_counter()

        elapsed = current_time - self.previous_time

        if elapsed > 0:
            self.fps = 1.0 / elapsed

        self.previous_time = current_time

        return round(self.fps, 1)