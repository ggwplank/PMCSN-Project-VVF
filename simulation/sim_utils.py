import random

from utils.constants import INF


# Simulazione del tempo di arrivo
def get_next_arrival_time(stream, mean_arrival_time):
    return stream.expovariate(1 / mean_arrival_time)


# Simulazione del tempo di servizio
def get_service_time(stream, mean_service_time):
    return stream.expovariate(1 / mean_service_time)


# Assegnazione del colore
def assign_color(stream, probabilities):
    p = stream.uniform(0, 100)
    if p < probabilities['red']:
        return "red"
    elif p < probabilities['yellow']:
        return "yellow"
    else:
        return "green"


def release_server(server):
    server.occupied = False
    server.end_service_time = INF


def preempt_current_job(server, t):
    print(f"Preempting current job {server.job_color.upper()} at time {t.current_time}")
    release_server(server)
