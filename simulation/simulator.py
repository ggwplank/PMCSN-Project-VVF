import os

from libs import rngs

from simulation.queue_manager import QueueManager
from simulation.sim_utils import get_next_arrival_time, get_service_time, assign_color, preempt_current_job, \
    fake_alarm_check, check_jobs
from simulation.event import Event
from simulation.server import Server, release_server

from utils.constants import *
from utils.file_manager import *
from utils.printer import *
from utils.statistics import Statistics

rngs.plantSeeds(SEED)

# stream 0 -> arrivi al sistema = arrivi hub
# stream 1 -> tempi di servizio hub
# stream 2 -> tempi di servizio red
# stream 3 -> tempi di servizio yellow
# stream 4 -> tempi di servizio green
# stream 5 -> assegnazione colore
# stream 6 -> probabilità di autorisoluzione
# stream 7 -> probabilità di fake alarm

# Inizializzazione degli Oggetti di Simulazione
queue_manager = QueueManager()  # Gestione delle code
stats = Statistics()  # Raccolta delle statistiche

# Inizializzazione dei server
servers_hub = [Server() for _ in range(HUB_SERVERS)]
operative_servers = [Server() for _ in range(OPERATIVE_SERVERS)]
squadra, modulo = operative_servers[0], operative_servers[1]
squadra.type, modulo.type = SQUADRA, MODULO

# Inizializzazione delle variabili di stato
squad_completion = INF


# Processa l'arrivo di un job all'hub
def process_job_arrival_at_hub(t, servers_hub):
    print(f"Job arrived at hub at time {t.current_time}")

    t.next_arrival = get_next_arrival_time(MEAN_ARRIVAL_TIME) + t.current_time

    # Trova il primo server libero
    free_server = next((server for server in servers_hub if not server.occupied), None)
    if free_server:
        free_server.occupied = True
        free_server.start_service_time = t.current_time

        service_time = get_service_time('hub')
        free_server.end_service_time = t.current_time + service_time
        t.hub_completion = free_server.end_service_time

        # stats
        stats.append_queue_time_list('hub', 0)
        stats.append_service_time_list('hub', service_time)
        stats.append_response_time_list('hub', service_time)
    else:
        queue_manager.add_to_queue('hub', t.current_time)

    update_completion_time(t)


# Processa il completamento di un job nell'hub
def process_job_completion_at_hub(t, next_event_function):
    # server che ha completato il job
    completed_server = next((server for server in servers_hub if server.end_service_time == t.current_time), None)
    if completed_server:
        release_server(completed_server)

        color = assign_color(CODE_ASSIGNMENT_PROBS)
        t.type = color
        print(f"Job in hub completed at time {t.current_time} and sent to sent to {color.upper()} queue")

        # ci sono job in coda
        if not queue_manager.is_queue_empty("hub"):
            next_job_time = queue_manager.get_from_queue('hub')

            completed_server.occupied = True
            completed_server.start_service_time = next_job_time

            service_time = get_service_time('hub')
            completed_server.end_service_time = t.current_time + service_time

            # stats
            stats.append_queue_time_list('hub', t.current_time - next_job_time)
            stats.append_service_time_list('hub', service_time)
            stats.append_response_time_list('hub', t.current_time - next_job_time + service_time)

        update_completion_time(t)
        next_event_function(t, color)  # assegnazione job a un colore

    update_completion_time(t)


def process_job_arrival_at_colors(t, color):
    # il server è libero, processa subito il job
    if not squadra.occupied or (color == 'green' and not modulo.occupied):
        start_service_time = t.current_time
        assign_server(t, color, start_service_time, t.current_time)
    else:  # il server è occupato, aggiungi il job alla coda del colore corrispondente
        assign_server(t, color, t.current_time, t.current_time)

    update_completion_time(t)


def assign_server(t, color, added_in_queue_time, current_time):
    # funzione per assegnare un server a un job, con gestione della prelazione
    if not squadra.occupied:
        squadra.job_color = color
        if color == 'green':
            color = 'green_squadra'
        squadra.occupied = True
        squadra.start_service_time = current_time
        service_time = get_service_time(color)
        # Controlliamo che non sia un fake alarm
        squadra.end_service_time = current_time + fake_alarm_check(color, service_time)

        # stats
        queue_time = current_time - added_in_queue_time
        stats.append_queue_time_list(color, queue_time)
        stats.append_service_time_list(color, service_time)
        stats.append_response_time_list(color, service_time + queue_time)

        print(
            f"Squadra assegnata al job di colore {color} con start {squadra.start_service_time}, con tempo di completamento {squadra.end_service_time}")

    else:
        # gestione della prelazione
        if color == 'red' and squadra.job_color in ['yellow', 'green']:
            preempt_current_job(squadra, t, stats, squadra.job_color, squadra.start_service_time, current_time - added_in_queue_time)
            assign_server(t, color, added_in_queue_time, current_time)
        elif color == 'yellow' and squadra.job_color == 'green':
            preempt_current_job(squadra, t, stats, squadra.job_color,squadra.start_service_time, current_time - added_in_queue_time)
            assign_server(t, color, added_in_queue_time, current_time)
        elif color == 'green' and not modulo.occupied:
            modulo.job_color = color
            color = 'green_modulo'

            modulo.occupied = True
            modulo.start_service_time = added_in_queue_time
            service_time = get_service_time(color)
            # Controlliamo che non sia un fake alarm
            modulo.end_service_time = current_time + fake_alarm_check(color, service_time)

            # stats
            queue_time = current_time - added_in_queue_time
            stats.append_queue_time_list(color, queue_time)
            stats.append_service_time_list(color, service_time)
            stats.append_response_time_list(color, service_time + queue_time)

            print(
                f"Modulo assegnato al job di colore {color} con start {modulo.start_service_time}, con tempo di completamento {modulo.end_service_time}")
        else:
            queue_manager.add_to_queue(color, added_in_queue_time)
            print(f"Job di colore {color} aggiunto alla coda poiché sia squadra che modulo sono occupati")

    update_completion_time(t)


def process_job_completion_at_colors(t, server):
    release_server(server)

    if server == squadra:
        for color in ['red', 'yellow', 'green']:
            # "squadra" gestisce i job in quest'ordine di priorità: red, yellow, green
            if not queue_manager.is_queue_empty(color):
                next_job_time = queue_manager.get_from_queue(color)
                assign_server(t, color, next_job_time, t.current_time)
                break
    elif server == modulo and not queue_manager.is_queue_empty('green'):  # "modulo" gestisce solo job green
        next_job_time = queue_manager.get_from_queue('green')
        assign_server(t, 'green', next_job_time, t.current_time)

    update_completion_time(t)

    # aggiorna il tempo di completamento per il job successivo in coda
    if server == squadra:
        t.red_completion = squadra.end_service_time if squadra.job_color == 'red' else INF
        t.yellow_completion = squadra.end_service_time if squadra.job_color == 'yellow' else INF
        t.green_completion_squadra = squadra.end_service_time if squadra.job_color == 'green' else INF
    elif server == modulo:
        t.green_completion_modulo = modulo.end_service_time


def update_completion_time(t):
    global squad_completion

    t.hub_completion = min((server.end_service_time for server in servers_hub if server.occupied), default=INF)

    if squadra.occupied:
        squad_completion = squadra.end_service_time
        t.red_completion = squadra.end_service_time if squadra.job_color == 'red' else INF
        t.yellow_completion = squadra.end_service_time if squadra.job_color == 'yellow' else INF
        t.green_completion_squadra = squadra.end_service_time if squadra.job_color == 'green' else INF
    else:
        t.red_completion = t.yellow_completion = t.green_completion_squadra = INF

    t.green_completion_modulo = modulo.end_service_time if modulo.occupied else INF


def infinite_simulation(batch_size, t):
    start_time = t.current_time

    while stats.job_arrived < batch_size:
        if check_jobs(t):
            break
        execute(t)

    stats.set_stop_time(t.current_time - start_time)
    return t


def finite_simulation(stop_time, t):
    stats.set_stop_time(stop_time)

    while t.current_time < stop_time:
        if check_jobs(t):
            break
        execute(t)


def execute(t):
    events = {
        'arrival': t.next_arrival,
        'hub_completion': t.hub_completion,
        'red_completion': t.red_completion,
        'yellow_completion': t.yellow_completion,
        'green_completion_squadra': t.green_completion_squadra,
        'green_completion_modulo': t.green_completion_modulo,
        'squad_completion': squad_completion
    }

    print_simulation_status(t, events)

    next_event_time = min(t.next_arrival, t.hub_completion, t.red_completion, t.yellow_completion,
                          t.green_completion_squadra, t.green_completion_modulo)
    t.current_time = next_event_time

    queue_manager.discard_job_from_red_queue()
    queue_manager.discard_job_from_yellow_queue()
    queue_manager.discard_job_from_green_queue()

    if t.current_time == t.next_arrival:
        stats.job_arrived += 1
        process_job_arrival_at_hub(t, servers_hub)
    elif t.current_time == t.hub_completion:
        process_job_completion_at_hub(t, process_job_arrival_at_colors)
    elif t.current_time == t.red_completion and squadra.job_color == 'red':
        stats.job_completed += 1
        process_job_completion_at_colors(t, squadra)
    elif t.current_time == t.yellow_completion and squadra.job_color == 'yellow':
        stats.job_completed += 1
        process_job_completion_at_colors(t, squadra)
    elif t.current_time == t.green_completion_squadra:
        stats.job_completed += 1
        process_job_completion_at_colors(t, squadra)
    elif t.current_time == t.green_completion_modulo:
        stats.job_completed += 1
        process_job_completion_at_colors(t, modulo)

    print_queue_status(queue_manager)
