import math
import scipy.stats as stats

from utils.constants import MEAN_HUB_SERVICE_TIME, HUB_SERVERS, LOC


class Statistics:
    def __init__(self):
        self.stop_time = None

        # hub
        self.N_queue_hub_list = []
        self.queue_hub_time_list = []
        self.service_hub_time_list = []
        self.response_hub_time_list = []
        self.hub_rho_list = []

        self.mean_N_queue_hub = 0
        self.mean_queue_hub_time = 0.0
        self.mean_service_hub_time = 0.0
        self.mean_response_hub_time = 0.0
        self.mean_hub_rho = 0.0

        # Intervalli di confidenza
        self.mean_queue_hub_time_confidence_interval = 0.0
        self.mean_N_queue_hub_confidence_interval = 0.0
        self.mean_service_hub_time_confidence_interval = 0.0
        self.mean_response_hub_time_confidence_interval = 0.0
        self.hub_rho_confidence_interval = 0.0

        # Red queue
        self.N_queue_red_list = []  # Numero di job in coda rossa
        self.queue_red_time_list = []  # Tempi di attesa in coda rossa
        self.service_red_time_list = []  # Tempi di servizio in coda rossa
        self.response_red_time_list = []  # Tempi di risposta in coda rossa
        self.red_rho_list = []  # Utilizzazione dei server nella coda rossa

        self.mean_N_queue_red = 0
        self.mean_queue_red_time = 0.0
        self.mean_service_red_time = 0.0
        self.mean_response_red_time = 0.0
        self.mean_red_rho = 0.0

        # Intervalli di confidenza per la coda rossa
        self.mean_queue_red_time_confidence_interval = 0.0
        self.mean_N_queue_red_confidence_interval = 0.0
        self.mean_service_red_time_confidence_interval = 0.0
        self.mean_response_red_time_confidence_interval = 0.0
        self.red_rho_confidence_interval = 0.0

    def set_stop_time(self, stop_time):
        self.stop_time = stop_time

    # ======
    # Metodi per aggiungere dati alle liste
    # ======
    def increment_total_N_queue_hub(self):
        self.N_queue_hub_list.append(1)

    def append_queue_hub_time_list(self, queue_hub_time):
        self.queue_hub_time_list.append(queue_hub_time)

    def append_service_hub_time_list(self, service_hub_time):
        self.service_hub_time_list.append(service_hub_time)

    def append_response_hub_time(self, response_time):
        self.response_hub_time_list.append(response_time)

    # ======
    # Metodi per calcolare le metriche medie
    # ======
    def calculate_mean_queue_hub_time(self):
        if len(self.queue_hub_time_list) > 0:
            total_queue_hub_time = sum(self.queue_hub_time_list)
            self.mean_queue_hub_time = total_queue_hub_time / len(self.queue_hub_time_list)
        else:
            self.mean_queue_hub_time = 0.0

    def calculate_mean_N_queue_hub(self):
        if self.stop_time > 0:
            total_N_queue_hub = sum(self.N_queue_hub_list)
            self.mean_N_queue_hub = total_N_queue_hub / self.stop_time
        else:
            self.mean_N_queue_hub = 0.0

    def calculate_mean_service_hub_time(self):
        if len(self.service_hub_time_list) > 0:
            total_service_hub_time = sum(self.service_hub_time_list)
            self.mean_service_hub_time = total_service_hub_time / len(self.service_hub_time_list)
        else:
            self.mean_service_hub_time = 0.0

    def calculate_mean_response_hub_time(self):
        if len(self.response_hub_time_list) > 0:
            total_response_hub_time = sum(self.response_hub_time_list)
            self.mean_response_hub_time = total_response_hub_time / len(self.response_hub_time_list)
        else:
            self.mean_response_hub_time = 0.0

    def calculate_hub_rho(self):
        if self.stop_time > 0 and HUB_SERVERS > 0:
            total_service_hub_time = sum(self.service_hub_time_list)
            self.mean_hub_rho = total_service_hub_time / (HUB_SERVERS * self.stop_time)
        else:
            self.mean_hub_rho = 0.0

    def increment_total_N_queue_red(self):
        self.N_queue_red_list.append(1)

    def append_queue_red_time_list(self, queue_red_time):
        self.queue_red_time_list.append(queue_red_time)

    def append_service_red_time_list(self, service_red_time):
        self.service_red_time_list.append(service_red_time)

    def append_response_red_time(self, response_time):
        self.response_red_time_list.append(response_time)

    def calculate_mean_queue_red_time(self):
        if len(self.queue_red_time_list) > 0:
            total_queue_red_time = sum(self.queue_red_time_list)
            self.mean_queue_red_time = total_queue_red_time / len(self.queue_red_time_list)
        else:
            self.mean_queue_red_time = 0.0

    def calculate_mean_N_queue_red(self):
        if self.stop_time > 0:
            total_N_queue_red = sum(self.N_queue_red_list)
            self.mean_N_queue_red = total_N_queue_red / self.stop_time
        else:
            self.mean_N_queue_red = 0.0

    def calculate_mean_service_red_time(self):
        if len(self.service_red_time_list) > 0:
            total_service_red_time = sum(self.service_red_time_list)
            self.mean_service_red_time = total_service_red_time / len(self.service_red_time_list)
        else:
            self.mean_service_red_time = 0.0

    def calculate_mean_response_red_time(self):
        if len(self.response_red_time_list) > 0:
            total_response_red_time = sum(self.response_red_time_list)
            self.mean_response_red_time = total_response_red_time / len(self.response_red_time_list)
        else:
            self.mean_response_red_time = 0.0

    def calculate_red_rho(self):
        if self.stop_time > 0:
            total_service_red_time = sum(self.service_red_time_list)
            self.mean_red_rho = total_service_red_time / self.stop_time
        else:
            self.mean_red_rho = 0.0

    # Calcolo delle statistiche di una singola run
    def calculate_run_statistics(self):
        self.calculate_mean_queue_hub_time()
        self.calculate_mean_N_queue_hub()
        self.calculate_mean_service_hub_time()
        self.calculate_mean_response_hub_time()
        self.calculate_hub_rho()

        self.calculate_mean_queue_red_time()
        self.calculate_mean_N_queue_red()
        self.calculate_mean_service_red_time()
        self.calculate_mean_response_red_time()
        self.calculate_red_rho()

        return {
            'mean_queue_hub_time': self.mean_queue_hub_time,
            'mean_N_queue_hub': self.mean_N_queue_hub,
            'mean_service_hub_time': self.mean_service_hub_time,
            'mean_response_hub_time': self.mean_response_hub_time,
            'hub_rho': self.mean_hub_rho,

            # Statistiche coda rossa
            'mean_queue_red_time': self.mean_queue_red_time,
            'mean_N_queue_red': self.mean_N_queue_red,
            'mean_service_red_time': self.mean_service_red_time,
            'mean_response_red_time': self.mean_response_red_time,
            'red_rho': self.mean_red_rho
        }

    def calculate_all_confidence_intervals(self):
        self.mean_queue_hub_time, self.mean_queue_hub_time_confidence_interval = calculate_confidence_interval(
            self.queue_hub_time_list)
        self.mean_N_queue_hub, self.mean_N_queue_hub_confidence_interval = calculate_confidence_interval(
            self.N_queue_hub_list)
        self.mean_service_hub_time, self.mean_service_hub_time_confidence_interval = calculate_confidence_interval(
            self.service_hub_time_list)
        self.mean_response_hub_time, self.mean_response_hub_time_confidence_interval = calculate_confidence_interval(
            self.response_hub_time_list)
        self.mean_hub_rho, self.hub_rho_confidence_interval = calculate_confidence_interval(self.hub_rho_list)

        # Intervalli di confidenza per la coda rossa
        self.mean_queue_red_time, self.mean_queue_red_time_confidence_interval = calculate_confidence_interval(
            self.queue_red_time_list)
        self.mean_N_queue_red, self.mean_N_queue_red_confidence_interval = calculate_confidence_interval(
            self.N_queue_red_list)
        self.mean_service_red_time, self.mean_service_red_time_confidence_interval = calculate_confidence_interval(
            self.service_red_time_list)
        self.mean_response_red_time, self.mean_response_red_time_confidence_interval = calculate_confidence_interval(
            self.response_red_time_list)
        self.mean_red_rho, self.red_rho_confidence_interval = calculate_confidence_interval(self.red_rho_list)

    # Reset delle statistiche per una nuova run
    def reset_statistics(self):
        self.N_queue_hub_list = []
        self.queue_hub_time_list = []
        self.service_hub_time_list = []
        self.response_hub_time_list = []
        self.hub_rho_list = []

        self.mean_queue_hub_time = 0.0
        self.mean_N_queue_hub = 0
        self.mean_service_hub_time = 0.0
        self.mean_response_hub_time = 0.0
        self.mean_hub_rho = 0.0

        # Resetta le variabili delle statistiche della coda rossa
        self.N_queue_red_list = []
        self.queue_red_time_list = []
        self.service_red_time_list = []
        self.response_red_time_list = []
        self.red_rho_list = []

        self.mean_queue_red_time = 0.0
        self.mean_N_queue_red = 0
        self.mean_service_red_time = 0.0
        self.mean_response_red_time = 0.0
        self.mean_red_rho = 0.0

        self.stop_time = None


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
