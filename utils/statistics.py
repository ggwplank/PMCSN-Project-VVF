import math
import scipy.stats as stats

from utils.constants import MEAN_HUB_SERVICE_TIME, HUB_SERVERS, LOC


class Statistics:
    def __init__(self):
        self.stop_time = None
        # Inizializzazione delle liste per ogni colore
        self.data = {
            'hub': {
                'N_queue_list': [],
                'queue_time_list': [],
                'service_time_list': [],
                'response_time_list': [],

                'mean_N_queue': 0,
                'mean_queue_hub_time': 0.0,
                'mean_service_time': 0.0,
                'mean_response_time': 0.0,
                'mean_rho': 0.0,

                'mean_queue_time_confidence_interval': 0.0,
                'mean_N_queue_confidence_interval': 0.0,
                'mean_service_time_confidence_interval': 0.0,
                'mean_response_time_confidence_interval': 0.0,
                'rho_confidence_interval': 0.0
            },
            'red': {
                'N_queue_list': [],
                'queue_time_list': [],
                'service_time_list': [],
                'response_time_list': [],

                'mean_N_queue': 0,
                'mean_queue_hub_time': 0.0,
                'mean_service_time': 0.0,
                'mean_response_time': 0.0,
                'mean_rho': 0.0,

                'mean_queue_time_confidence_interval': 0.0,
                'mean_N_queue_confidence_interval': 0.0,
                'mean_service_time_confidence_interval': 0.0,
                'mean_response_time_confidence_interval': 0.0,
                'rho_confidence_interval': 0.0
            },
            'yellow': {
                'N_queue_list': [],
                'queue_time_list': [],
                'service_time_list': [],
                'response_time_list': [],

                'mean_N_queue': 0,
                'mean_queue_hub_time': 0.0,
                'mean_service_time': 0.0,
                'mean_response_time': 0.0,
                'mean_rho': 0.0,

                'mean_queue_time_confidence_interval': 0.0,
                'mean_N_queue_confidence_interval': 0.0,
                'mean_service_time_confidence_interval': 0.0,
                'mean_response_time_confidence_interval': 0.0,
                'rho_confidence_interval': 0.0
            },
            'green': {
                'N_queue_list': [],
                'queue_time_list': [],
                'service_time_list': [],
                'response_time_list': [],

                'mean_N_queue': 0,
                'mean_queue_hub_time': 0.0,
                'mean_service_time': 0.0,
                'mean_response_time': 0.0,
                'mean_rho': 0.0,

                'mean_queue_time_confidence_interval': 0.0,
                'mean_N_queue_confidence_interval': 0.0,
                'mean_service_time_confidence_interval': 0.0,
                'mean_response_time_confidence_interval': 0.0,
                'rho_confidence_interval': 0.0
            }
        }

    def set_stop_time(self, stop_time):
        self.stop_time = stop_time

    # ======
    # Metodi per aggiungere dati alle liste
    # ======
    def increment_total_N_queue(self, color):
        self.data[color]['N_queue_list'].append(1)

    def append_queue_time_list(self, color, queue_time):
        self.data[color]['queue_time_list'].append(queue_time)

    def append_service_time_list(self, color, service_time):
        self.data[color]['service_time_list'].append(service_time)

    def append_response_time_list(self, color, response_time):
        self.data[color]['response_time_list'].append(response_time)

    # ======
    # Metodi per calcolare le metriche medie
    # ======

    def calculate_mean_queue_time(self, color):
        queue_times = self.data[color]['queue_time_list']
        if len(queue_times) > 0:
            total_queue_time = sum(queue_times)
            self.data[color]['mean_queue_time'] = total_queue_time / len(queue_times)
        else:
            self.data[color]['mean_queue_time'] = 0.0

    def calculate_mean_N_queue(self, color):
        if self.stop_time > 0:
            total_N_queue = sum(self.data[color]['N_queue_list'])
            self.data[color]['mean_N_queue'] = total_N_queue / self.stop_time
        else:
            self.data[color]['mean_N_queue'] = 0.0

    def calculate_mean_service_time(self, color):
        service_times = self.data[color]['service_time_list']
        if len(service_times) > 0:
            total_service_time = sum(service_times)
            self.data[color]['mean_service_time'] = total_service_time / len(service_times)
        else:
            self.data[color]['mean_service_time'] = 0.0

    def calculate_mean_response_time(self, color):
        response_times = self.data[color]['response_time_list']
        if len(response_times) > 0:
            total_response_time = sum(response_times)
            self.data[color]['mean_response_time'] = total_response_time / len(response_times)
        else:
            self.data[color]['mean_response_time'] = 0.0

    def calculate_rho(self, color):
        if self.stop_time > 0:
            total_service_time = sum(self.data[color]['service_time_list'])
            if color == 'hub':
                self.data[color]['mean_rho'] = total_service_time / (HUB_SERVERS * self.stop_time)
            else:
                self.data[color]['mean_rho'] = total_service_time / self.stop_time
        else:
            self.data[color]['mean_rho'] = 0.0

    # ======
    # Calcolo delle statistiche di una singola run
    # ======
    def calculate_run_statistics(self):
        for color in self.data.keys():
            self.calculate_mean_queue_time(color)
            self.calculate_mean_N_queue(color)
            self.calculate_mean_service_time(color)
            self.calculate_mean_response_time(color)
            self.calculate_rho(color)

        return {color: {
            'mean_queue_time': self.data[color]['mean_queue_time'],
            'mean_N_queue': self.data[color]['mean_N_queue'],
            'mean_service_time': self.data[color]['mean_service_time'],
            'mean_response_time': self.data[color]['mean_response_time'],
            'mean_rho': self.data[color]['mean_rho']
        } for color in self.data.keys()}

    # ======
    # Calcolo degli intervalli di confidenza per ogni colore
    # ======
    def calculate_all_confidence_intervals(self):
        for color in self.data.keys():
            self.data[color]['mean_queue_time'], self.data[color][
                'mean_queue_time_confidence_interval'] = calculate_confidence_interval(
                self.data[color]['queue_time_list'])
            self.data[color]['mean_N_queue'], self.data[color][
                'mean_N_queue_confidence_interval'] = calculate_confidence_interval(
                self.data[color]['N_queue_list'])
            self.data[color]['mean_service_time'], self.data[color][
                'mean_service_time_confidence_interval'] = calculate_confidence_interval(
                self.data[color]['service_time_list'])
            self.data[color]['mean_response_time'], self.data[color][
                'mean_response_time_confidence_interval'] = calculate_confidence_interval(
                self.data[color]['response_time_list'])
            self.data[color]['mean_rho'], self.data[color]['rho_confidence_interval'] = calculate_confidence_interval(
                self.data[color]['rho_list'])

        # ======
        # Reset delle statistiche per una nuova run
        # ======

    def reset_statistics(self):
        for color in self.data.keys():
            self.data[color]['N_queue_list'] = []
            self.data[color]['queue_time_list'] = []
            self.data[color]['service_time_list'] = []
            self.data[color]['response_time_list'] = []
            self.data[color]['rho_list'] = []

            self.data[color]['mean_queue_time'] = 0.0
            self.data[color]['mean_N_queue'] = 0
            self.data[color]['mean_service_time'] = 0.0
            self.data[color]['mean_response_time'] = 0.0
            self.data[color]['mean_rho'] = 0.0

        self.stop_time = None


#TODO: rifare intervalli di confidenza
def calculate_confidence_interval(data):
    n = len(data)
    if n == 0:
        return 0.0, 0.0  # nessun dato, restituisce intervallo nullo

    mean, standard_deviation = calculate_mean_and_standard_deviation(data)

    # Gradi di libertà = n - 1
    degrees_of_freedom = n - 1

    # Ottieni il valore t* per il livello di confidenza desiderato
    t_star = stats.t.ppf((1 + LOC) / 2, degrees_of_freedom)

    # Calcolo dell'intervallo di confidenza
    margin_of_error = t_star * (standard_deviation / math.sqrt(n))

    return mean, margin_of_error


def calculate_mean_and_standard_deviation(data):
    n = len(data)
    if n == 0:
        return 0.0, 0.0

    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)  # Varianza campionaria
    standard_deviation = math.sqrt(variance)
    return mean, standard_deviation
