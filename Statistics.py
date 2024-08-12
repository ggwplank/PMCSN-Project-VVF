# statistics.py

class Statistics:
    def __init__(self):
        self.total_response_time = 0.0
        self.completed_jobs = 0

    def record_response_time(self, response_time):
        self.total_response_time += response_time
        self.completed_jobs += 1

    def mean_response_time(self):
        if self.completed_jobs > 0:
            return self.total_response_time / self.completed_jobs
        else:
            return 0.0
