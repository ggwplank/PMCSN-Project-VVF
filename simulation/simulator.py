import random

from simulation.queueManager import QueueManager
from utils.constants import *
from utils.printer import *
from utils.statistics import Statistics

from simulation.event import Event
from simulation.server import Server

# Creazione degli stream separati
stream_arrival = random.Random()  # Per generare i tempi di arrivo
stream_service_hub = random.Random()  # Per generare i tempi di servizio per centralino/hub
stream_service_red = random.Random()  # Per generare i tempi di servizio per codice rosso
stream_service_yellow = random.Random()  # Per generare i tempi di servizio per codice giallo
stream_service_green = random.Random()  # Per generare i tempi di servizio per codice verde
stream_code_assignment = random.Random()  # Per assegnare i codici colore

# Inizializza il queueManager
queue_manager = QueueManager()

# Inizializza le statistiche
stats = Statistics()

# Variabili di stato del sistema
servers_hub = [Server() for _ in range(HUB_SERVERS)]
operative_servers = [Server() for _ in range(OPERATIVE_SERVERS)]
squadra = operative_servers[0]
squadra.type = SQUADRA
modulo = operative_servers[1]
modulo.type = MODULO

jobs_in_hub = 0
jobs_in_red = 0
jobs_in_yellow = 0
jobs_in_green = 0

# Dizionario che mappa i colori agli stream
streams_colors = {
    'red': stream_service_red,
    'yellow': stream_service_yellow,
    'green': stream_service_green,
}


# Simulazione del tempo di arrivo
def generate_next_arrival_time():
    return stream_arrival.expovariate(1 / MEAN_ARRIVAL_TIME)


# Simulazione del tempo di servizio
def get_service_time(stream, params):
    return stream.expovariate(1 / params)


# Assegnazione del colore
def assign_color():
    p = stream_code_assignment.uniform(0, 100)
    if p < CODE_ASSIGNMENT_PROBS['red']:
        return "red"
    elif p < CODE_ASSIGNMENT_PROBS['yellow']:
        return "yellow"
    else:
        return "green"


# Processamento di un arrivo nell'hub
def process_arrival_at_hub(t, servers_hub):
    global jobs_in_hub
    print(f"Job arrived at hub at time {t.current_time}")
    jobs_in_hub += 1
    t.next_arrival = generate_next_arrival_time() + t.current_time

    # Trova il primo server libero
    index = next((i for i, server in enumerate(servers_hub) if not server.occupied), None)

    if index is not None:  # Se c'è un server libero
        servers_hub[index].end_service_time = t.current_time + get_service_time(stream_service_hub, HUB_SERVERS)
        servers_hub[index].occupied = True
        servers_hub[index].start_service_time = t.current_time
        t.hub_completion = servers_hub[index].end_service_time
    else:  # Nessun server libero, il job va in coda
        queue_manager.add_to_queue('hub', t.current_time)

    update_completion_time(t)


def process_job_completion_at_hub(t, servers, next_event_function):
    global jobs_in_hub

    # Trova il server che ha completato il job
    index = next((i for i, server in enumerate(servers) if server.end_service_time == t.current_time), None)
    if index is not None:
        response_time = t.current_time - servers[index].start_service_time
        stats.add_hub_response_time(response_time)

        servers[index].occupied = False
        servers[index].end_service_time = INF

        print(f"Job in hub completed at time {t.current_time}")
        color = assign_color()
        t.type = color
        jobs_in_hub -= 1

        # Se ci sono job in coda, assegna il prossimo job al server che si è liberato
        if not queue_manager.is_queue_empty("hub"):
            next_job_time = queue_manager.get_from_queue('hub')
            service_time = get_service_time(stream_service_hub, HUB_SERVERS)
            servers[index].end_service_time = t.current_time + service_time
            servers[index].occupied = True
            servers[index].start_service_time = t.current_time  # Assicurati di usare il tempo corrente

        update_completion_time(t)
        # Assegna il job completato a una coda colorata

        next_event_function(t, color)

    update_completion_time(t)


def update_completion_time(t):
    if any(server.occupied for server in servers_hub):
        t.hub_completion = min(server.end_service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF  # Se nessun server è occupato, imposta il completamento dell'hub a INF

    if squadra.occupied:
        if squadra.job_color == 'red':
            t.red_completion = squadra.end_service_time
        else:
            t.red_completion = INF
        if squadra.job_color == 'yellow':
            t.yellow_completion = squadra.end_service_time
        else:
            t.yellow_completion = INF
    else:
        t.red_completion = INF
        t.yellow_completion = INF

    if modulo.occupied:
        t.green_completion = modulo.end_service_time
    else:
        t.green_completion = INF


def process_arrival_at_colors(t, color):
    global jobs_in_green, jobs_in_yellow, jobs_in_red
    if color == 'red':
        jobs_in_red += 1
    elif color == 'yellow':
        jobs_in_yellow += 1
    elif color == 'green':
        jobs_in_green += 1

    if queue_manager.is_queue_empty(color):

        start_service_time = t.current_time

        assign_server(t, color, start_service_time)

    else:
        next_job_time = queue_manager.get_from_queue(color)

        assign_server(t, color, next_job_time)

    # Imposta il tempo di completamento dinamicamente in base al colore
    if color == 'red':
        t.red_completion = squadra.end_service_time
    elif color == 'yellow':
        t.yellow_completion = squadra.end_service_time
    elif color == 'green':
        t.green_completion = min(squadra.end_service_time, modulo.end_service_time)
    else:
        queue_manager.add_to_queue(color, t.current_time)


def assign_server(t, color, start_service_time):
    if not squadra.occupied:
        squadra.end_service_time = t.current_time + get_service_time(streams_colors[color],
                                                                     # TODO metti come servente la squadra
                                                                     5 * 10)
        squadra.occupied = True
        squadra.start_service_time = start_service_time
        squadra.job_color = color

    elif squadra.occupied and not color == 'green':
        queue_manager.add_to_queue(color, t.current_time)

    elif squadra.occupied and color == 'green':

        if not modulo.occupied:
            modulo.end_service_time = t.current_time + get_service_time(streams_colors[color],
                                                                        # TODO metti come servente il modulo
                                                                        5 * 10)
            squadra.occupied = True
            modulo.start_service_time = start_service_time
            modulo.job_color = color
        else:
            queue_manager.add_to_queue(color, t.current_time)


# un job nei colori viene completato
def process_job_completion_at_colors(t, server, color):
    global jobs_in_red, jobs_in_yellow, jobs_in_green
    print(f"Completed {color} job at time {t.current_time}")

    if color == 'red':
        jobs_in_red -= 1
    elif color == 'yellow':
        jobs_in_yellow -= 1
    elif color == 'green':
        jobs_in_green -= 1

    response_time = t.current_time - server.start_service_time
    stats.add_system_response_time(response_time)  # non c'è distinzione di colore
    stats.add_color_response_time(color, response_time)

    server.occupied = False
    server.end_service_time = INF

    if not queue_manager.is_queue_empty(color):
        next_job_time = queue_manager.get_from_queue(color)
        assign_server(t, color, next_job_time)

    update_completion_time(t)


def run_simulation(stop_time):
    global jobs_in_hub, jobs_in_red, jobs_in_yellow, jobs_in_green

    t = Event(0, generate_next_arrival_time(), INF, INF, INF, INF, INF)

    while t.current_time < stop_time:
        # Gestisci la situazione in cui tutti i tempi sono INF (nessun evento futuro)
        if all(x == INF for x in
               [t.next_arrival, t.hub_completion, t.red_completion, t.yellow_completion, t.green_completion]):
            print("Simulation complete: no more events.")
            break

        events = {
            'arrival': t.next_arrival,
            'hub_completion': t.hub_completion,
            'red_completion': t.red_completion,
            'yellow_completion': t.yellow_completion,
            'green_completion': t.green_completion
        }

        print_simulation_status(t, events)

        next_event_time = min(t.next_arrival, t.hub_completion,
                              t.red_completion, t.yellow_completion, t.green_completion)

        t.current_time = next_event_time

        if t.current_time == t.next_arrival:
            process_arrival_at_hub(t, servers_hub)
        elif t.current_time == t.hub_completion:
            process_job_completion_at_hub(t, servers_hub, process_arrival_at_colors)
        elif t.current_time == t.red_completion:
            process_job_completion_at_colors(t, squadra, 'red')
        elif t.current_time == t.yellow_completion:
            process_job_completion_at_colors(t, squadra, 'yellow')
        elif t.current_time == t.green_completion:
            if not modulo.occupied:
                process_job_completion_at_colors(t, squadra, 'green')
            elif squadra.occupied and modulo.occupied and not squadra.job_color == 'green':
                process_job_completion_at_colors(t, modulo, 'green')

        print_queue_status(queue_manager)


run_simulation(100)

"""
# Stampa delle statistiche
print_section_title("SYSTEM STATISTICS")
print(f"Total Jobs Completed: {stats.completed_jobs}")
print(f"Mean Response Time: {stats.mean_response_time()}\n")

print_section_title("HUB QUEUE STATISTICS")
print(f"Total hub Jobs Completed: {len(stats.hub_jobs_response_times)}")
print(f"Mean hub Response Time: {stats.get_hub_mean_response_time()}")
print(f"Response Times:")
for response_time in stats.hub_jobs_response_times:
    print(f"{response_time}")
print()

print_queue_statistics("red", stats.red_jobs_response_times, stats)
print_queue_statistics("yellow", stats.yellow_jobs_response_times, stats)
print_queue_statistics("green", stats.green_jobs_response_times, stats)
"""

print_separator()
print("End of Simulation Report")
