from simulator.libs import rngs, rvms

from simulator.simulation.server import release_server

from simulator.utils.constants import MEAN_HUB_SERVICE_TIME, MEAN_YELLOW_SERVICE_TIME, MEAN_RED_SERVICE_TIME, \
    MEAN_GREEN_SERVICE_TIME, FAKE_ALLARM_RED_PROB, FAKE_ALLARM_YELLOW_PROB, FAKE_ALLARM_GREEN_PROB, INF

streams = {
    'hub': 1,
    'red': 2,
    'yellow': 3,
    'green_squadra': 4,
    'green_modulo': 4
}

service_rates = {
    'hub': MEAN_HUB_SERVICE_TIME,
    'red': MEAN_RED_SERVICE_TIME,
    'yellow': MEAN_YELLOW_SERVICE_TIME,
    'green_squadra': MEAN_GREEN_SERVICE_TIME,
    'green_modulo': MEAN_GREEN_SERVICE_TIME
}


# Simulazione del tempo di arrivo
def get_next_arrival_time(mean_arrival_time):
    rngs.selectStream(0)
    return rvms.idfExponential(mean_arrival_time, rngs.random())


# Simulazione del tempo di servizio
def get_service_time(stream):
    rngs.selectStream(streams[stream])
    service_time = rvms.idfExponential(service_rates[stream], rngs.random())

    # esponenziale troncata, che tiene sempre conto del tempo necessario all'arrivo sul luogo
    if stream != "hub":
        return service_time + 25

    return service_time


# Simulazione del fake alarm, tempo di servizio = 0, se è fake imposta a 0 il tempo di servizio, altrimenti non viene
# cambiato
def fake_alarm_check(queue_color, service_time, probability=None):
    if queue_color == 'red':
        probability = FAKE_ALLARM_RED_PROB
    elif queue_color == 'yellow':
        probability = FAKE_ALLARM_YELLOW_PROB
    elif queue_color == 'green_squadra' or queue_color == 'green_modulo':
        probability = FAKE_ALLARM_GREEN_PROB

    rngs.selectStream(6)
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


def preempt_current_job(server, t, stats, color, start_service_time, queue_time):
    print(f"Preempting current job {server.job_color.upper()} at time {t.current_time}")
    if color == 'green':
        color = 'green_squadra'
    stats.data[color]['service_time_list'].pop(0)
    stats.data[color]['service_time_list'].append(t.current_time - start_service_time)
    stats.data[color]['response_time_list'].pop(0)
    #stats.data[color]['response_time_list'].append((t.current_time-start_service_time)+ queue_time)
    release_server(server)


def check_jobs(t):
    if all(x == INF for x in
           [t.next_arrival, t.hub_completion, t.red_completion,
            t.yellow_completion, t.green_completion_squadra, t.green_completion_modulo]):
        print("Simulation complete: no more events.")
        return True
