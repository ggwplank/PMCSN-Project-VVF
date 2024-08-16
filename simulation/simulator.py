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
servers_hub = [Server() for _ in range(SERVERS_1)]
servers_red = [Server() for _ in range(SERVERS_2)]
servers_yellow = [Server() for _ in range(SERVERS_3)]
servers_green = [Server() for _ in range(SERVERS_4)]

jobs_in_hub = 0
jobs_in_red = 0
jobs_in_yellow = 0
jobs_in_green = 0

# Dizionario che mappa i colori ai rispettivi server
servers_colors = {
    "red": servers_red,
    "yellow": servers_yellow,
    "green": servers_green,
}

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
    return stream.expovariate(1 / params / 10)


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
    print(f"Job arrived at hub at time {t.current}")
    jobs_in_hub += 1
    t.arrival = generate_next_arrival_time() + t.current

    # Trova il primo server libero
    index = next((i for i, server in enumerate(servers_hub) if not server.occupied), None)

    if index is not None:  # Se c'è un server libero
        if queue_manager.is_queue_empty("hub"):  # Nessun job in coda
            servers_hub[index].service_time = t.current + get_service_time(stream_service_hub, SERVERS_1)
            servers_hub[index].occupied = True
            servers_hub[index].start_time = t.current
            t.hub_completion = servers_hub[index].service_time
        else:  # C'è un job in coda
            next_job_time = queue_manager.get_from_queue('hub')
            servers_hub[index].service_time = t.current + get_service_time(stream_service_hub, SERVERS_1)
            servers_hub[index].occupied = True
            servers_hub[index].start_time = next_job_time
            t.hub_completion = servers_hub[index].service_time
    else:  # Nessun server libero, il job va in coda
        queue_manager.add_to_queue('hub', t.current)

    update_completion_time(t)


def process_job_completion_at_hub(t, servers, next_event_function):
    global jobs_in_hub

    # Trova il server che ha completato il job
    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)
    if index is not None:
        response_time = t.current - servers[index].start_time
        stats.add_hub_response_time(response_time)

        servers[index].occupied = False
        servers[index].service_time = INF

        if servers == servers_hub:
            print(f"Job in hub completed at time {t.current}")
            color = assign_color()
            t.color = color
            jobs_in_hub -= 1

            if not queue_manager.is_queue_empty("hub"):
                next_job_time = queue_manager.get_from_queue('hub')
                service_time = get_service_time(stream_service_hub, SERVERS_1)
                servers[index].service_time = t.current + service_time
                servers[index].occupied = True
                servers[index].start_time = next_job_time

            update_completion_time(t)
            # Assegna il job completato a una coda colorata

            next_event_function(t, servers_colors[color], color)

    update_completion_time(t)


def update_completion_time(t):
    # Dopo ogni completamento, aggiornare i tempi di completamento per evitare loop
    if any(server.occupied for server in servers_red):
        t.red_completion = min(server.service_time for server in servers_red if server.occupied)
    else:
        t.red_completion = INF

    if any(server.occupied for server in servers_yellow):
        t.yellow_completion = min(server.service_time for server in servers_yellow if server.occupied)
    else:
        t.yellow_completion = INF

    if any(server.occupied for server in servers_green):
        t.green_completion = min(server.service_time for server in servers_green if server.occupied)
    else:
        t.green_completion = INF

    if any(server.occupied for server in servers_hub):
        t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF


def process_arrival_at_colors(t, servers, color):
    global jobs_in_green, jobs_in_yellow, jobs_in_red
    if color == 'red':
        jobs_in_red += 1
    elif color == 'yellow':
        jobs_in_yellow += 1
    elif color == 'green':
        jobs_in_green += 1

    index = next((i for i, server in enumerate(servers) if not server.occupied), None)

    if index is not None:
        if queue_manager.is_queue_empty(color):
            servers[index].service_time = t.current + get_service_time(streams_colors[color], len(servers) * 10)
            servers[index].occupied = True
            servers[index].start_time = t.current

        else:
            next_job_time = queue_manager.get_from_queue(color)
            servers[index].service_time = t.current + get_service_time(streams_colors[color], len(servers) * 10)
            servers[index].occupied = True
            servers[index].start_time = next_job_time

        # Imposta il tempo di completamento dinamicamente in base al colore
        if color == 'red':
            t.red_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'yellow':
            t.yellow_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'green':
            t.green_completion = min(server.service_time for server in servers if server.occupied)
    else:
        queue_manager.add_to_queue(color, t.current)

    #update_completion_time(t)


# Un generico job viene completato
# TODO forse è meglio solo job_completion?
def process_job_completion_at_colors(t, servers, color):
    global jobs_in_red, jobs_in_yellow, jobs_in_green
    print(f"Completed {color} job at time {t.current}")

    if color == 'red':
        jobs_in_red -= 1
    elif color == 'yellow':
        jobs_in_yellow -= 1
    elif color == 'green':
        jobs_in_green -= 1

    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)
    if index is not None:
        response_time = t.current - servers[index].start_time
        stats.add_system_response_time(response_time)  # non c'è distinzione di colore
        stats.add_color_response_time(color, response_time)

        servers[index].occupied = False
        servers[index].service_time = INF

        if not queue_manager.is_queue_empty(color):
            next_job_time = queue_manager.get_from_queue(color)
            servers[index].service_time = t.current + get_service_time(streams_colors[color], len(servers) * 10)
            servers[index].occupied = True
            servers[index].start_time = next_job_time
    update_completion_time(t)


def run_simulation(stop_time):
    global jobs_in_hub, jobs_in_red, jobs_in_yellow, jobs_in_green

    t = Event(0, generate_next_arrival_time(), INF, INF, INF, INF, INF)

    while t.current < stop_time:
        # Gestisci la situazione in cui tutti i tempi sono INF (nessun evento futuro)
        if all(x == INF for x in
               [t.arrival, t.hub_completion, t.red_completion, t.yellow_completion, t.green_completion]):
            print("Simulation complete: no more events.")
            break

        events = {
            'arrival': t.arrival,
            'hub_completion': t.hub_completion,
            'red_completion': t.red_completion,
            'yellow_completion': t.yellow_completion,
            'green_completion': t.green_completion
        }

        print_simulation_status(t, events)

        next_event_time = min(t.arrival, t.hub_completion,
                              t.red_completion, t.yellow_completion, t.green_completion)

        t.current = next_event_time

        if t.current == t.arrival:
            process_arrival_at_hub(t, servers_hub)
        elif t.current == t.hub_completion:
            process_job_completion_at_hub(t, servers_hub, process_arrival_at_colors)
        elif t.current == t.red_completion:
            process_job_completion_at_colors(t, servers_red, 'red')
        elif t.current == t.yellow_completion:
            process_job_completion_at_colors(t, servers_yellow, 'yellow')
        elif t.current == t.green_completion:
            process_job_completion_at_colors(t, servers_green, 'green')

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
