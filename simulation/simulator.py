from libs import rngs
from simulation.queue_manager import QueueManager
from simulation.sim_utils import get_next_arrival_time, get_service_time, assign_color, release_server, \
    preempt_current_job

from utils.constants import *
from utils.printer import *
from utils.statistics import Statistics

from simulation.event import Event
from simulation.server import Server

# seed
rngs.plantSeeds(SEED)

"""
# Creazione degli stream separati
stream_arrival = rngs.selectStream(0)  # Genera tempi di arrivo
stream_service_hub = rngs.selectStream(1)  # Genera tempi di servizio per centralino/hub
stream_service_red = rngs.selectStream(2)  # Genera tempi di servizio per codice rosso
stream_service_yellow = rngs.selectStream(3)  # Genera tempi di servizio per codice giallo
stream_service_green = rngs.selectStream(4)  # Genera tempi di servizio per codice verde
stream_code_assignment = rngs.selectStream(5)  # Assegna i codici colore
"""

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
jobs_in_hub = 0
jobs_in_red = 0
jobs_in_yellow = 0
jobs_in_green = 0

"""
# Dizionario che mappa i colori agli stream
streams_colors = {
    'red': stream_service_red,
    'yellow': stream_service_yellow,
    'green': stream_service_green,
}
"""


# Processa l'arrivo di un job all'hub
def process_job_arrival_at_hub(t, servers_hub):
    global jobs_in_hub
    print(f"Job arrived at hub at time {t.current_time}")
    jobs_in_hub += 1

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
        stats.increment_total_N_queue_hub()
        stats.append_queue_hub_time_list(0)
        stats.append_service_hub_time_list(service_time)
        stats.append_response_hub_time(service_time)

    else:
        queue_manager.add_to_queue('hub', t.current_time)

    update_completion_time(t)


# Processa il completamento di un job nell'hub
def process_job_completion_at_hub(t, next_event_function):
    global jobs_in_hub

    # Trova il server che ha completato il job
    completed_server = next((server for server in servers_hub if server.end_service_time == t.current_time), None)
    if completed_server:
        jobs_in_hub -= 1
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
            stats.increment_total_N_queue_hub()
            stats.append_queue_hub_time_list(t.current_time - next_job_time)
            stats.append_service_hub_time_list(service_time)
            stats.append_response_hub_time(t.current_time - next_job_time + service_time)

        update_completion_time(t)
        next_event_function(t, color)  # Assegna il job completato a una coda colorata

    update_completion_time(t)


def process_job_arrival_at_colors(t, color):
    global jobs_in_green, jobs_in_yellow, jobs_in_red
    if color == 'red':
        jobs_in_red += 1
    elif color == 'yellow':
        jobs_in_yellow += 1
    elif color == 'green':
        jobs_in_green += 1

    # il server è libero, processa subito il job
    if not squadra.occupied or (color == 'green' and not modulo.occupied):
        start_service_time = t.current_time
        assign_server(t, color, start_service_time, t.current_time)
    else:  # il server è occupato, aggiungi il job alla coda del colore corrispondente
        assign_server(t, color, t.current_time, t.current_time)

    update_completion_time(t)


def assign_server(t, color, start_service_time, current_time):
    # funzione per assegnare un server a un job, con gestione della prelazione
    if not squadra.occupied:
        squadra.occupied = True
        squadra.start_service_time = start_service_time
        squadra.end_service_time = current_time + get_service_time(color)
        squadra.job_color = color
        print(
            f"Squadra assegnata al job di colore {color} con start {squadra.start_service_time}, con tempo di completamento {squadra.end_service_time}")
    else:
        # gestione della prelazione
        if color == 'red' and squadra.job_color in ['yellow', 'green']:
            preempt_current_job(squadra, t)
            assign_server(t, color, start_service_time, current_time)
        elif color == 'yellow' and squadra.job_color == 'green':
            preempt_current_job(squadra, t)
            assign_server(t, color, start_service_time, current_time)
        elif color == 'green' and not modulo.occupied:
            modulo.end_service_time = current_time + get_service_time(color)
            modulo.occupied = True
            modulo.start_service_time = start_service_time
            modulo.job_color = color
            print(
                f"Modulo assegnato al job di colore {color} con start {modulo.start_service_time}, con tempo di completamento {modulo.end_service_time}")
        else:
            queue_manager.add_to_queue(color, start_service_time)
            print(f"Job di colore {color} aggiunto alla coda poiché sia squadra che modulo sono occupati")

    update_completion_time(t)


def process_job_completion_at_colors(t, server, color):
    global jobs_in_red, jobs_in_yellow, jobs_in_green
    if color == 'red':
        jobs_in_red -= 1
    elif color == 'yellow':
        jobs_in_yellow -= 1
    elif color == 'green':
        jobs_in_green -= 1

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


def run_simulation(stop_time):
    stats.set_stop_time(stop_time)

    t = Event(0, get_next_arrival_time(MEAN_ARRIVAL_TIME), INF, INF, INF, INF, INF)

    while t.current_time < stop_time:
        if all(x == INF for x in
               [t.next_arrival, t.hub_completion, t.red_completion,
                t.yellow_completion, t.green_completion_squadra, t.green_completion_modulo]):
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

        next_event_time = min(t.next_arrival, t.hub_completion, t.red_completion, t.yellow_completion,
                              t.green_completion_squadra, t.green_completion_modulo)
        t.current_time = next_event_time

        queue_manager.discard_job_from_green_queue()
        queue_manager.discard_job_from_yellow_queue()

        if t.current_time == t.next_arrival:
            process_job_arrival_at_hub(t, servers_hub)
        elif t.current_time == t.hub_completion:
            process_job_completion_at_hub(t, process_job_arrival_at_colors)
        elif t.current_time == t.red_completion and squadra.job_color == 'red':
            process_job_completion_at_colors(t, squadra, 'red')
        elif t.current_time == t.yellow_completion and squadra.job_color == 'yellow':
            process_job_completion_at_colors(t, squadra, 'yellow')
        elif t.current_time == t.green_completion_squadra:
            process_job_completion_at_colors(t, squadra, 'green')
        elif t.current_time == t.green_completion_modulo:
            process_job_completion_at_colors(t, modulo, 'green')

        print_queue_status(queue_manager)


# TODO: resetta il sistema tra una run e l'altra
filename = "statistics.txt"

# Esegui la simulazione 3 volte e salva i risultati in un file di testo
with open(filename, "w") as file:
    for i in range(10):
        run_simulation(1000)
        prova = stats.calculate_statistics()  # Suppongo che `calculate_statistics` ritorni un dizionario con le statistiche

        file.write(f"Risultati della simulazione {i + 1}:\n")
        for key, value in prova.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")  # Aggiungi una linea vuota tra le simulazioni

print_separator()
print("End of Simulation Report")
