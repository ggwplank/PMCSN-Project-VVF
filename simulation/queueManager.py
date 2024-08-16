class QueueManager:
    def __init__(self):
        self.queues = {
            "hub": [],
            "red": [],
            "yellow": [],
            "green": [],
            "white": []
        }

    def add_job_to_queue(self, color, job_time):
        if color in self.queues:
            self.queues[color].append(job_time)
        else:
            print(f"Error: Invalid color '{color}'")

    def get_next_job_from_queue(self, color):
        if color in self.queues and self.queues[color]:
            return self.queues[color].pop(0)
        else:
            return None

    def is_queue_empty(self, color):
        if color in self.queues:
            return len(self.queues[color]) == 0
        else:
            print(f"Error: Invalid color '{color}'")
            return True

    def get_queue_length(self, color):
        if color in self.queues:
            return len(self.queues[color])
        else:
            print(f"Error: Invalid color '{color}'")
            return 0