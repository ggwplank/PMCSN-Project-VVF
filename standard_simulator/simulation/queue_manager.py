import random
from collections import deque


class QueueManager:
    def __init__(self):
        self.queues = {
            "hub": deque(),
            "red": deque(),
            "yellow": deque(),
            "green": deque()
        }

    def validate_color(self, color):
        if color not in self.queues:
            raise ValueError(f"Error: Invalid color '{color}'")
        return True

    def add_to_queue(self, color, job_time):
        if self.validate_color(color):
            self.queues[color].append(job_time)

    def get_from_queue(self, color):
        if self.validate_color(color) and self.queues[color]:
            return self.queues[color].popleft()
        return None

    def is_queue_empty(self, color):
        if self.validate_color(color):
            return len(self.queues[color]) == 0

    def get_queue_length(self, color):
        if self.validate_color(color):
            return len(self.queues[color])

    def reset_queues(self):
        for key, queue in self.queues.items():
            queue.clear()

    def check_queues(self):
        for key, queue in self.queues.items():
            if len(queue) != 0:
                return False
        return True
