# statistics.py

def evaluate_queue_mean_response_time(jobs_response_time):
    code_mean_response_time = 0

    if len(jobs_response_time) > 0:
        for response_time in jobs_response_time:
            code_mean_response_time += response_time
        return code_mean_response_time / len(jobs_response_time)
    else:
        return 0.0


class Statistics:
    def __init__(self):
        self.total_response_time = 0.0
        self.completed_jobs = 0

        self.hub_jobs_response_time = []
        self.red_jobs_response_time = []
        self.yellow_jobs_response_time = []
        self.green_jobs_response_time = []
        self.white_jobs_response_time = []

    def system_response_time(self, response_time):
        self.total_response_time += response_time
        self.completed_jobs += 1

    def mean_response_time(self):
        if self.completed_jobs > 0:
            return self.total_response_time / self.completed_jobs
        else:
            return 0.0

    def hub_response_time(self, response_time):
        self.hub_jobs_response_time.append(response_time)

    def hub_mean_response_time(self):
        return evaluate_queue_mean_response_time(self.hub_jobs_response_time)

    def code_response_time(self, color, response_time):
        if color == 'red':
            self.red_jobs_response_time.append(response_time)
        elif color == 'yellow':
            self.yellow_jobs_response_time.append(response_time)
        elif color == 'green':
            self.green_jobs_response_time.append(response_time)
        elif color == 'white':
            self.white_jobs_response_time.append(response_time)

    def code_mean_response_time(self, color):
        if color == 'red':
            return evaluate_queue_mean_response_time(self.red_jobs_response_time)
        elif color == 'yellow':
            return evaluate_queue_mean_response_time(self.yellow_jobs_response_time)
        elif color == 'green':
            return evaluate_queue_mean_response_time(self.green_jobs_response_time)
        elif color == 'white':
            return evaluate_queue_mean_response_time(self.white_jobs_response_time)
