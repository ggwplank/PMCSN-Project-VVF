import random

from libs import rvms, rngs
from utils.constants import INF, MEAN_HUB_SERVICE_TIME, MEAN_YELLOW_SERVICE_TIME, MEAN_RED_SERVICE_TIME, \
    MEAN_GREEN_SERVICE_TIME

streams = {
    'hub': 1,
    'red': 2,
    'yellow': 3,
    'green': 4
}

service_rates = {
    'hub': MEAN_HUB_SERVICE_TIME,
    'red': MEAN_RED_SERVICE_TIME,
    'yellow': MEAN_YELLOW_SERVICE_TIME,
    'green': MEAN_GREEN_SERVICE_TIME
}


# Simulazione del tempo di arrivo
def get_next_arrival_time(mean_arrival_time):
    rngs.selectStream(0)
    return rvms.idfExponential(1 / mean_arrival_time, rngs.random())


# Simulazione del tempo di servizio
def get_service_time(stream):
    rngs.selectStream(streams[stream])
    return rvms.idfExponential(1 / service_rates[stream], rngs.random())


# Assegnazione del colore
def assign_color(probabilities):
    rngs.selectStream(5)
    p = rvms.idfUniform(0, 100, rngs.random())
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
