from better_simulator.libs import rngs

from better_simulator.simulation.queue_manager import QueueManager
from better_simulator.simulation.sim_utils import get_next_arrival_time, get_service_time, assign_color, \
    preempt_current_job, \
    fake_alarm_check, check_jobs
from better_simulator.simulation.server import Server, release_server

from better_simulator.utils.constants import *
from better_simulator.utils.printer import *
from better_simulator.utils.statistics import Statistics

rngs.plantSeeds(SEED)

# stream 0 -> arrivi al sistema = arrivi hub
# stream 1 -> tempi di servizio hub
# stream 2 -> tempi di servizio red
# stream 3 -> tempi di servizio orange
# stream 4 -> tempi di servizio yellow
# stream 5 -> tempi di servizio green
# stream 6 -> assegnazione colore
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
modulo_completion = INF


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
    if not squadra.occupied or (color in ['green', 'yellow'] and not modulo.occupied):
        start_service_time = t.current_time
        assign_server(t, color, start_service_time, t.current_time)
    else:  # il server è occupato, aggiungi il job alla coda del colore corrispondente
        assign_server(t, color, t.current_time, t.current_time)

    update_completion_time(t)


def assign_server(t, color, added_in_queue_time, current_time):
    # funzione per assegnare un server a un job, con gestione della prelazione
    if not squadra.occupied and color != 'green':
        squadra.job_color = color
        if color == 'yellow':
            color += '_squadra'
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
        if color == 'red' and squadra.job_color in ['orange', 'yellow']:
            preempt_current_job(squadra, t, stats, squadra.job_color, squadra.start_service_time)
            assign_server(t, color, added_in_queue_time, current_time)
        elif color == 'orange' and squadra.job_color == 'yellow':
            preempt_current_job(squadra, t, stats, squadra.job_color, squadra.start_service_time)
            assign_server(t, color, added_in_queue_time, current_time)
        elif color == 'yellow' and modulo.job_color == 'green' and modulo.occupied:
            preempt_current_job(modulo, t, stats, modulo.job_color, modulo.start_service_time)
            assign_server(t, color, added_in_queue_time, current_time)
        elif color in ['yellow', 'green'] and not modulo.occupied:
            modulo.job_color = color
            color = color + '_modulo'

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
        for color in ['red', 'orange', 'yellow', 'green']:
            # "squadra" gestisce i job in quest'ordine di priorità: red, orange, yellow, green
            if not queue_manager.is_queue_empty(color):
                next_job_time = queue_manager.get_from_queue(color)
                assign_server(t, color, next_job_time, t.current_time)
                break
    elif server == modulo:
        for color in ['yellow', 'green']:
            if not queue_manager.is_queue_empty(color):
                next_job_time = queue_manager.get_from_queue(color)
                assign_server(t, color, next_job_time, t.current_time)
                break

    update_completion_time(t)

    # aggiorna il tempo di completamento per il job successivo in coda
    if server == squadra:
        t.red_completion = squadra.end_service_time if squadra.job_color == 'red' else INF
        t.orange_completion = squadra.end_service_time if squadra.job_color == 'orange' else INF
        t.yellow_completion_squadra = squadra.end_service_time if squadra.job_color == 'yellow' else INF
    elif server == modulo:
        t.green_completion_modulo = modulo.end_service_time if modulo.job_color == 'green' else INF
        t.yellow_completion_modulo = modulo.end_service_time if modulo.job_color == 'yellow' else INF


def update_completion_time(t):
    t.hub_completion = min((server.end_service_time for server in servers_hub if server.occupied), default=INF)

    if squadra.occupied:
        global squad_completion
        squad_completion = squadra.end_service_time
        t.red_completion = squadra.end_service_time if squadra.job_color == 'red' else INF
        t.orange_completion = squadra.end_service_time if squadra.job_color == 'orange' else INF
        t.yellow_completion_squadra = squadra.end_service_time if squadra.job_color == 'yellow' else INF
    else:
        t.red_completion = t.orange_completion = t.yellow_completion_squadra = t.green_completion_squadra = INF

    if modulo.occupied:
        global modulo_completion
        modulo_completion = modulo.end_service_time
        t.yellow_completion_modulo = modulo.end_service_time if modulo.job_color == 'yellow' else INF
        t.green_completion_modulo = modulo.end_service_time if modulo.job_color == 'green' else INF
    else:
        t.yellow_completion_modulo = t.green_completion_modulo = INF


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
        'orange_completion': t.orange_completion,
        'yellow_completion_squadra': t.yellow_completion_squadra,
        'yellow_completion_modulo': t.yellow_completion_modulo,
        'green_completion_modulo': t.green_completion_modulo,
        'squad_completion': squad_completion
    }

    print_simulation_status(t, events)

    next_event_time = min(t.next_arrival, t.hub_completion, t.red_completion, t.orange_completion,
                          t.yellow_completion_squadra, t.yellow_completion_modulo,
                          t.green_completion_modulo)
    t.current_time = next_event_time

    if t.current_time == t.next_arrival:
        stats.job_arrived += 1
        process_job_arrival_at_hub(t, servers_hub)
    elif t.current_time == t.hub_completion:
        process_job_completion_at_hub(t, process_job_arrival_at_colors)
    elif t.current_time == t.red_completion and squadra.job_color == 'red':
        stats.job_completed += 1
        process_job_completion_at_colors(t, squadra)
    elif t.current_time == t.orange_completion and squadra.job_color == 'orange':
        stats.job_completed += 1
        process_job_completion_at_colors(t, squadra)
    elif t.current_time == t.yellow_completion_squadra and squadra.job_color == 'yellow':
        stats.job_completed += 1
        process_job_completion_at_colors(t, squadra)
    elif t.current_time == t.yellow_completion_modulo and modulo.job_color == 'yellow':
        stats.job_completed += 1
        process_job_completion_at_colors(t, modulo)
    elif t.current_time == t.green_completion_modulo and modulo.job_color == 'green':
        stats.job_completed += 1
        process_job_completion_at_colors(t, modulo)

    print_queue_status(queue_manager)
