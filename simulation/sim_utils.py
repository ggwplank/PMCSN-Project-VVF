import random

from libs import rvms, rngs

from simulation.server import release_server

from utils.constants import MEAN_HUB_SERVICE_TIME, MEAN_YELLOW_SERVICE_TIME, MEAN_RED_SERVICE_TIME, \
    MEAN_GREEN_SERVICE_TIME, FAKE_ALLARM_RED_PROB, FAKE_ALLARM_YELLOW_PROB, FAKE_ALLARM_GREEN_PROB

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
    return rvms.idfExponential(mean_arrival_time, rngs.random())


# Simulazione del tempo di servizio
def get_service_time(stream):
    rngs.selectStream(streams[stream])
    return rvms.idfExponential(service_rates[stream], rngs.random())


# Simulazione del fake alarm, tempo di servizio = 0, se è fake imposta a 0 il tempo di servizio, altrimenti non viene
# cambiato
def fake_alarm_check(queue_color, service_time, probability=None):
    if queue_color == 'red':
        probability = FAKE_ALLARM_RED_PROB
    elif queue_color == 'yellow':
        probability = FAKE_ALLARM_YELLOW_PROB
    elif queue_color == 'green':
        probability = FAKE_ALLARM_GREEN_PROB

    rngs.selectStream(7)
    p = rvms.idfUniform(0, 100, rngs.random())
    if p < probability:
        service_time = 0
        print(f"{queue_color} job is a FAKE ALARM!")
    return service_time


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


def preempt_current_job(server, t):
    print(f"Preempting current job {server.job_color.upper()} at time {t.current_time}")
    release_server(server)
