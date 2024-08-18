from utils.constants import MEAN_HUB_SERVICE_TIME, HUB_SERVERS


class Statistics:
    def __init__(self):
        self.stop_time = None

        # hub
        self.total_queue_hub_time = 0.0
        self.total_N_queue_hub = 0
        self.total_service_hub_time = 0.0
        self.total_response_hub_time = 0.0

        self.mean_queue_hub_time = 0.0
        self.mean_N_queue_hub = 0
        self.mean_service_hub_time = 0.0
        self.mean_response_hub_time = 0.0
        self.hub_rho = 0.0

    def set_stop_time(self, stop_time):
        self.stop_time = stop_time

    def increment_total_N_queue_hub(self):
        self.total_N_queue_hub += 1

    def increment_queue_hub_time(self, queue_hub_time):
        self.total_queue_hub_time += queue_hub_time

    def increment_service_hub_time(self, service_hub_time):
        self.total_service_hub_time += service_hub_time

    def increment_response_hub_time(self, response_time):
        self.total_response_hub_time += response_time

    def calculate_mean_queue_hub_time(self):
        self.mean_queue_hub_time = self.total_queue_hub_time / self.total_N_queue_hub

    def calculate_mean_N_queue_hub(self):
        self.mean_N_queue_hub = self.total_N_queue_hub / self.stop_time

    def calculate_mean_service_hub_time(self):
        self.mean_service_hub_time = self.total_service_hub_time / self.total_N_queue_hub

    def calculate_mean_response_hub_time(self):
        self.mean_response_hub_time = self.total_response_hub_time / self.total_N_queue_hub

    def calculate_hub_rho(self):
        self.hub_rho = ((self.total_service_hub_time / (MEAN_HUB_SERVICE_TIME * HUB_SERVERS)) / self.stop_time)

    def calculate_statistics(self):
        self.calculate_mean_queue_hub_time()
        self.calculate_mean_N_queue_hub()
        self.calculate_mean_service_hub_time()
        self.calculate_mean_response_hub_time()
        self.calculate_hub_rho()
