from better_simulator.libs import rngs, rvms

from better_simulator.simulation.server import release_server

from better_simulator.utils.constants import MEAN_HUB_SERVICE_TIME, MEAN_YELLOW_SERVICE_TIME, MEAN_RED_SERVICE_TIME, \
    MEAN_GREEN_SERVICE_TIME, FAKE_ALLARM_RED_PROB, FAKE_ALLARM_YELLOW_PROB, FAKE_ALLARM_GREEN_PROB, INF, \
    MEAN_ORANGE_SERVICE_TIME, FAKE_ALLARM_ORANGE_PROB

streams = {
    'hub': 1,
    'red': 2,
    'orange': 3,
    'yellow_squadra': 4,
    'yellow_modulo': 4,
    'green_modulo': 5
}

service_rates = {
    'hub': MEAN_HUB_SERVICE_TIME,
    'red': MEAN_RED_SERVICE_TIME,
    'orange': MEAN_ORANGE_SERVICE_TIME,
    'yellow_squadra': MEAN_YELLOW_SERVICE_TIME,
    'yellow_modulo': MEAN_YELLOW_SERVICE_TIME,
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
    elif queue_color == 'orange':
        probability = FAKE_ALLARM_ORANGE_PROB
    elif queue_color == 'yellow_squadra' or queue_color == 'yellow_modulo':
        probability = FAKE_ALLARM_YELLOW_PROB
    elif queue_color == 'green_modulo':
        probability = FAKE_ALLARM_GREEN_PROB

    rngs.selectStream(7)
    p = rvms.idfUniform(0, 100, rngs.random())
    if p < probability:
        service_time = 25
        print(f"{queue_color} job is a FAKE ALARM!")
    return service_time


# Assegnazione del colore
def assign_color(probabilities):
    rngs.selectStream(6)
    p = rvms.idfUniform(0, 100, rngs.random())
    if p < probabilities['red']:
        return "red"
    elif p < probabilities['orange']:
        return "orange"
    elif p < probabilities['yellow']:
        return "yellow"
    else:
        return "green"


def preempt_current_job(server, t, stats, color, start_service_time):
    print(f"Preempting current job {server.job_color.upper()} at time {t.current_time}")
    if server.type == "squadra" and color == 'yellow':
        color += "_squadra"
    elif server.type == "modulo" and color in ['yellow', 'green']:
        color += "_modulo"

    stats.data[color]['service_time_list'].pop(0)
    stats.data[color]['service_time_list'].append(t.current_time - start_service_time)
    stats.data[color]['response_time_list'].pop(0)
    release_server(server)


def check_jobs(t):
    if all(x == INF for x in
           [t.next_arrival, t.hub_completion, t.red_completion, t.orange_completion,
            t.yellow_completion_squadra, t.yellow_completion_modulo,
            t.green_completion_modulo]):
        print("Simulation complete: no more events.")
        return True
