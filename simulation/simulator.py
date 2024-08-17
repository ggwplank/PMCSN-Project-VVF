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

#Tempo di completamento della squadra
squad_completion = INF

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
        print(f"job sent at {color}")
        jobs_in_hub -= 1

        # Se ci sono job in coda, assegna il prossimo job al server che si è liberato
        if not queue_manager.is_queue_empty("hub"):
            next_job_time = queue_manager.get_from_queue('hub')
            service_time = get_service_time(stream_service_hub, HUB_SERVERS)
            servers[index].end_service_time = t.current_time + service_time
            servers[index].occupied = True
            servers[index].start_service_time = next_job_time  # Assicurati di usare il tempo corrente

        update_completion_time(t)
        # Assegna il job completato a una coda colorata

        next_event_function(t, color)

    update_completion_time(t)


def process_arrival_at_colors(t, color):
    global jobs_in_green, jobs_in_yellow, jobs_in_red
    if color == 'red':
        jobs_in_red += 1
    elif color == 'yellow':
        jobs_in_yellow += 1
    elif color == 'green':
        jobs_in_green += 1

    # Se il server è libero, processa subito il job
    if not squadra.occupied or (color == 'green' and not modulo.occupied):
        start_service_time = t.current_time
        assign_server(t, color, start_service_time, t.current_time)
    else:
        # Altrimenti, aggiungilo alla coda del colore corrispondente
        queue_manager.add_to_queue(color, t.current_time)

    # Aggiorna i tempi di completamento
    update_completion_time(t)


def assign_server(t, color, start_service_time, current_time):
    if not squadra.occupied:
        service_time = get_service_time(streams_colors[color], 5 * 10)
        squadra.end_service_time = current_time + service_time
        squadra.occupied = True
        squadra.start_service_time = start_service_time
        squadra.job_color = color
        print(
            f"Squadra assegnata al job di colore {color} con start {squadra.start_service_time}, con tempo di completamento {squadra.end_service_time}")

    elif squadra.occupied and color == 'green':
        if not modulo.occupied:
            modulo.end_service_time = current_time + get_service_time(streams_colors[color], 5 * 10)
            modulo.occupied = True
            modulo.start_service_time = start_service_time
            modulo.job_color = color
            print(
                f"Modulo assegnato al job di colore {color} con start {modulo.start_service_time}, con tempo di completamento {modulo.end_service_time}")
        else:
            queue_manager.add_to_queue(color, start_service_time)
            print(f"Job di colore {color} aggiunto alla coda poiché sia squadra che modulo sono occupati")
    else:
        queue_manager.add_to_queue(color, start_service_time)
        print(f"Job di colore {color} aggiunto alla coda poiché la squadra è occupata")

    update_completion_time(t)


def process_job_completion_at_colors(t, server, color):
    global jobs_in_red, jobs_in_yellow, jobs_in_green
    print(f"Completato job di colore {color} al tempo {t.current_time} (Server: {server.type})")

    if color == 'red':
        jobs_in_red -= 1
    elif color == 'yellow':
        jobs_in_yellow -= 1
    elif color == 'green':
        jobs_in_green -= 1

    response_time = t.current_time - server.start_service_time
    stats.add_system_response_time(response_time)
    stats.add_color_response_time(color, response_time)

    server.occupied = False
    server.end_service_time = INF

    if server == squadra:
        # La squadra gestisce i job in quest'ordine di priorità: red, yellow, green
        if not queue_manager.is_queue_empty('red'):
            next_job_time = queue_manager.get_from_queue('red')
            assign_server(t, 'red', next_job_time, t.current_time)
        elif not queue_manager.is_queue_empty('yellow'):
            next_job_time = queue_manager.get_from_queue('yellow')
            assign_server(t, 'yellow', next_job_time, t.current_time)
        elif not queue_manager.is_queue_empty('green'):
            next_job_time = queue_manager.get_from_queue('green')
            assign_server(t, 'green', next_job_time, t.current_time)
    elif server == modulo:
        # Il modulo gestisce solo job green
        if not queue_manager.is_queue_empty('green'):
            next_job_time = queue_manager.get_from_queue('green')
            assign_server(t, 'green', next_job_time, t.current_time)

    update_completion_time(t)

    # Assicurati di aggiornare il tempo di completamento per il job successivo in coda
    if server == squadra:
        t.red_completion = squadra.end_service_time if squadra.job_color == 'red' else INF
        t.yellow_completion = squadra.end_service_time if squadra.job_color == 'yellow' else INF
        t.green_completion_squadra = squadra.end_service_time if squadra.job_color == 'green' else INF
    elif server == modulo:
        t.green_completion_modulo = modulo.end_service_time


def update_completion_time(t):

    global squad_completion

    if any(server.occupied for server in servers_hub):
        t.hub_completion = min(server.end_service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF  # Se nessun server è occupato, imposta il completamento dell'hub a INF

    if squadra.occupied:
        squad_completion = squadra.end_service_time
        t.red_completion = squadra.end_service_time if squadra.job_color == 'red' else INF
        t.yellow_completion = squadra.end_service_time if squadra.job_color == 'yellow' else INF
        t.green_completion_squadra = squadra.end_service_time if squadra.job_color == 'green' else INF
    else:
        t.red_completion = INF
        t.yellow_completion = INF
        t.green_completion_squadra = INF

    if modulo.occupied:
        t.green_completion_modulo = modulo.end_service_time
    else:
        t.green_completion_modulo = INF


def run_simulation(stop_time):
    global jobs_in_hub, jobs_in_red, jobs_in_yellow, jobs_in_green

    t = Event(0, generate_next_arrival_time(), INF, INF, INF, INF, INF)

    while t.current_time < stop_time:
        # Gestisci la situazione in cui tutti i tempi sono INF (nessun evento futuro)
        if all(x == INF for x in
               [t.next_arrival, t.hub_completion, t.red_completion, t.yellow_completion, t.green_completion_squadra, t.green_completion_modulo]):
            print("Simulation complete: no more events.")
            break

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

        next_event_time = min(t.next_arrival, t.hub_completion,
                              t.red_completion, t.yellow_completion, t.green_completion_squadra, t.green_completion_modulo)

        t.current_time = next_event_time

        if t.current_time == t.next_arrival:
            process_arrival_at_hub(t, servers_hub)
        elif t.current_time == t.hub_completion:
            process_job_completion_at_hub(t, servers_hub, process_arrival_at_colors)
        elif t.current_time == t.red_completion and squadra.job_color == 'red':
            process_job_completion_at_colors(t, squadra, 'red')
        elif t.current_time == t.yellow_completion and squadra.job_color == 'yellow':
            process_job_completion_at_colors(t, squadra, 'yellow')
        elif t.current_time == t.green_completion_squadra:
            process_job_completion_at_colors(t, squadra, 'green')
        elif t.current_time == t.green_completion_modulo:
            process_job_completion_at_colors(t, modulo, 'green')

        print_queue_status(queue_manager)

run_simulation(500)

print_separator()
print("End of Simulation Report")
