import random
from collections import deque

from utils.constants import AUTORESOLUTION_GREEN_PROB, AUTORESOLUTION_YELLOW_PROB


class QueueManager:
    def __init__(self):
        self.queues = {
            "hub": deque(),  #deque per ottimizzare le operazioni di append e pop
            "red": deque(),
            "yellow": deque(),
            "green": deque()
        }

    def validate_color(self, color):
        """Verifica se il colore specificato è valido."""
        if color not in self.queues:
            raise ValueError(f"Error: Invalid color '{color}'")
        return True

    def add_to_queue(self, color, job_time):
        """Aggiunge un job alla coda specificata dal colore."""
        if self.validate_color(color):
            self.queues[color].append(job_time)

    def get_from_queue(self, color):
        """Rimuove e restituisce il primo job dalla coda specificata dal colore."""
        if self.validate_color(color) and self.queues[color]:
            return self.queues[color].popleft()
        return None

    def is_queue_empty(self, color):
        """Verifica se la coda specificata dal colore è vuota."""
        if self.validate_color(color):
            return len(self.queues[color]) == 0

    def get_queue_length(self, color):
        """Restituisce la lunghezza della coda specificata dal colore."""
        if self.validate_color(color):
            return len(self.queues[color])

    def discard_job_from_queue(self, queue_color, probability):
        deque = self.queues[queue_color]
        jobs_to_remove = []  # lista temporanea per i job da rimuovere

        for job in deque:
            if random.uniform(0, 100) < probability:
                print(f"{job} removed from {queue_color} queue, AUTORESOLVED!")
                jobs_to_remove.append(job)

        # rimozione dei job dalla coda specificata
        for job in jobs_to_remove:
            deque.remove(job)

        # aggiornamento della coda specificata
        self.queues[queue_color] = deque

    def discard_job_from_green_queue(self):
        self.discard_job_from_queue("green", AUTORESOLUTION_GREEN_PROB)

    def discard_job_from_yellow_queue(self):
        self.discard_job_from_queue("yellow", AUTORESOLUTION_YELLOW_PROB)