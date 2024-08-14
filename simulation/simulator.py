import random

from utils.constants import *
from utils.printer import *
from utils.statistics import Statistics

from simulation.event import Event
from simulation.server import Server

# Creazione degli stream separati
stream_arrival = random.Random()  # Per generare i tempi di arrivo
stream_service_hub = random.Random()  # Per generare i tempi di servizio per centralino/hub
stream_service_red = random.Random()  # Per generare i tempi di servizio per emergenza massima/codice rosso
stream_service_yellow = random.Random()  # Per generare i tempi di servizio per emergenza alta/codice giallo
stream_service_green = random.Random()  # Per generare i tempi di servizio per emergenza media/codice verde
stream_service_white = random.Random()  # Per generare i tempi di servizio per emergenza bassa/codice bianco
stream_code_assignment = random.Random()  # Per assegnare i codici colore

# Inizializza le statistiche
stats = Statistics()

# Variabili di stato del sistema
servers_hub = [Server() for _ in range(SERVERS_1)]
servers_red = [Server() for _ in range(SERVERS_2)]
servers_yellow = [Server() for _ in range(SERVERS_3)]
servers_green = [Server() for _ in range(SERVERS_4)]
servers_white = [Server() for _ in range(SERVERS_5)]

jobs_in_hub = 0
jobs_in_red = 0
jobs_in_yellow = 0
jobs_in_green = 0
jobs_in_white = 0

# Dizionario che mappa i colori ai rispettivi server
servers_colors = {
    "red": servers_red,
    "yellow": servers_yellow,
    "green": servers_green,
    "white": servers_white,
}

# Dizionario che mappa i colori agli stream
streams_colors = {
    'red': stream_service_red,
    'yellow': stream_service_yellow,
    'green': stream_service_green,
    'white': stream_service_white
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
    elif p < CODE_ASSIGNMENT_PROBS['green']:
        return "green"
    else:
        return "white"


# Processamento di un arrivo nell'hub
def process_arrival_at_hub(t, servers_hub):
    # TODO t -> event ??
    global jobs_in_hub
    print(f"Job arrived at hub at time {t.current}\n")
    jobs_in_hub += 1
    t.arrival = generate_next_arrival_time() + t.current

    index = next((i for i, server in enumerate(servers_hub) if not server.occupied), None)
    if index is not None:
        # TODO perché ci sommiamo il tempo corrente? Se è per la next-event, dobbiamo cambiare nome perché così
        # troppo ambiguo
        servers_hub[index].service_time = t.current + get_service_time(stream_service_hub, SERVERS_1)
        servers_hub[index].occupied = True

        # Registra l'istante di tempo in cui il job riceve servizio #TODO GIUSTO??
        servers_hub[index].start_time = t.current

        # TODO perché prendiamo il tempo di servizio minore tra i serventi dell'hub occupati?
        t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF  # non ci sono serventi liberi
        # TODO ma quindi non lo mettiamo in coda? che fine fa il job?


def process_job_completion_at_hub(t, servers, next_event_function):
    global jobs_in_hub

    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)
    if index is not None:
        response_time = t.current - servers[index].start_time
        stats.add_hub_response_time(response_time)

        servers[index].occupied = False
        servers[index].service_time = INF

        if servers == servers_hub:
            print(f"Job in hub completed at time {t.current}\n")
            color = assign_color()
            t.color = color
            jobs_in_hub -= 1

            # TODO controllo evitabile? Quando ci viene dato un colore inatteso?
            if color in servers_colors:
                next_event_function(t, servers_colors[color], color)

            # Aggiorna il tempo di completamento del hub
            if any(server.occupied for server in servers_hub):
                t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
            else:
                t.hub_completion = INF

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

    if any(server.occupied for server in servers_white):
        t.white_completion = min(server.service_time for server in servers_white if server.occupied)
    else:
        t.white_completion = INF

    if any(server.occupied for server in servers_hub):
        t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF


# Un generico job viene completato
# TODO forse è meglio solo job_completion?
def process_job_completion_at_colors(t, servers, color):
    global jobs_in_red, jobs_in_yellow, jobs_in_green, jobs_in_white
    print(f"Completed {color} job at time {t.current}\n")

    if color == 'red':
        jobs_in_red -= 1
    elif color == 'yellow':
        jobs_in_yellow -= 1
    elif color == 'green':
        jobs_in_green -= 1
    elif color == 'white':
        jobs_in_white -= 1

    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)
    if index is not None:
        response_time = t.current - servers[index].start_time
        stats.add_system_response_time(response_time)  # non c'è distinzione di colore
        stats.add_color_response_time(color, response_time)

        servers[index].occupied = False
        servers[index].service_time = INF

    # Aggiorna il tempo di completamento basato sul colore
    if any(server.occupied for server in servers):
        if color == 'red':
            t.red_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'yellow':
            t.yellow_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'green':
            t.green_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'white':
            t.white_completion = min(server.service_time for server in servers if server.occupied)
    else:
        if color == 'red':
            t.red_completion = INF
        elif color == 'yellow':
            t.yellow_completion = INF
        elif color == 'green':
            t.green_completion = INF
        elif color == 'white':
            t.white_completion = INF


def next_event_function(t, servers, color):
    index = next((i for i, server in enumerate(servers) if not server.occupied), None)
    if index is not None:
        stream = streams_colors[color]

        #TODO perché ci sommiamo il tempo corrente?
        servers[index].service_time = t.current + get_service_time(stream, len(servers))
        servers[index].occupied = True
        servers[index].start_time = t.current  # Registra l'inizio del servizio
        #TODO è l'inizio del servizio o l'arrivo al sistema?

        # Aggiorna il tempo di completamento in base al colore
        if color == 'red':
            t.red_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'yellow':
            t.yellow_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'green':
            t.green_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'white':
            t.white_completion = min(server.service_time for server in servers if server.occupied)
    else:
        # nessun servente è libero, il tempo di completamento è infinito
        #TODO di nuovo, nessuna coda?
        if color == 'red':
            t.red_completion = INF
        elif color == 'yellow':
            t.yellow_completion = INF
        elif color == 'green':
            t.green_completion = INF
        elif color == 'white':
            t.white_completion = INF


def run_simulation(stop_time):
    global jobs_in_hub, jobs_in_red, jobs_in_yellow, jobs_in_green, jobs_in_white

    t = Event(0, generate_next_arrival_time(), INF, INF, INF, INF, INF)

    while t.current < stop_time:
        # Gestisci la situazione in cui tutti i tempi sono INF (nessun evento futuro)
        if all(x == INF for x in
               [t.arrival, t.hub_completion, t.red_completion, t.yellow_completion, t.green_completion,
                t.white_completion]):
            print("Simulation complete: no more events.")
            break

            # Prepara i dati per la stampa
        events = {
            'arrival': t.arrival,
            'hub_completion': t.hub_completion,
            'red_completion': t.red_completion,
            'yellow_completion': t.yellow_completion,
            'green_completion': t.green_completion,
            'white_completion': t.white_completion
        }

        print_simulation_status(t, events)

        next_event_time = min(t.arrival, t.hub_completion,
                              t.red_completion, t.yellow_completion, t.green_completion, t.white_completion)

        t.current = next_event_time

        if t.current == t.arrival:
            process_arrival_at_hub(t, servers_hub)
        elif t.current == t.hub_completion:
            process_job_completion_at_hub(t, servers_hub, next_event_function)
        elif t.current == t.red_completion:
            process_job_completion_at_colors(t, servers_red, 'red')
        elif t.current == t.yellow_completion:
            process_job_completion_at_colors(t, servers_yellow, 'yellow')
        elif t.current == t.green_completion:
            process_job_completion_at_colors(t, servers_green, 'green')
        elif t.current == t.white_completion:
            process_job_completion_at_colors(t, servers_white, 'white')


run_simulation(50)

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
print_queue_statistics("white", stats.white_jobs_response_times, stats)

print_separator()
print("End of Simulation Report")
