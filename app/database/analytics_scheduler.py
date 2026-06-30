import time


class AnalyticsScheduler:

    def __init__(self, interval=5):

        self.interval = interval

        self.last_save_time = time.time()

    def should_save(self):

        current_time = time.time()

        if current_time - self.last_save_time >= self.interval:

            self.last_save_time = current_time
            return True

        return False