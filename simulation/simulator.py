import random

from utils.statistics import Statistics
from simulation.event import Event
from simulation.server import Server

from utils.constants import *

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

hub_number = 0
red_number = 0
yellow_number = 0
green_number = 0
white_number = 0


# Simulazione del tempo di arrivo
def get_arrival():
    return stream_arrival.expovariate(1 / MEAN_ARRIVAL_TIME)  # Es: tempo medio tra arrivi = 5 minuti


# Simulazione del tempo di servizio
def get_service(stream, params):
    return stream.expovariate(1 / params)  # Es: servizio medio


# Assegnazione del codice
def assign_code():
    p = stream_code_assignment.uniform(0, 100)
    if p < CODE_ASSIGNMENT_PROBS['red']:
        return "red"
    elif p < CODE_ASSIGNMENT_PROBS['yellow']:
        return "yellow"
    elif p < CODE_ASSIGNMENT_PROBS['green']:
        return "green"
    else:
        return "white"


# Processamento dell'arrivo nell'hub
def process_arrival(t, servers_hub):
    global hub_number
    print(f"Job arrived at time {t.current}\n")
    hub_number += 1
    t.arrival = get_arrival() + t.current

    index = next((i for i, server in enumerate(servers_hub) if not server.occupied), None)
    if index is not None:

        servers_hub[index].service_time = t.current + get_service(stream_service_hub, SERVERS_1)
        servers_hub[index].occupied = True

        servers_hub[index].start_time = t.current  # Registra l'inizio del servizio

        t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF  # Non ci sono servitori liberi


# Processamento generico del job completato
def process_completion(t, servers, color):
    global red_number, yellow_number, green_number, white_number
    print(f"Completed {color} job at time {t.current}\n")

    if color == 'red':
        red_number -= 1
    elif color == 'yellow':
        yellow_number -= 1
    elif color == 'green':
        green_number -= 1
    elif color == 'white':
        white_number -= 1

    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)
    if index is not None:
        response_time = t.current - servers[index].start_time
        stats.add_system_response_time(response_time)  # Registra il tempo di risposta
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


# Dizionario che mappa i colori alle funzioni di gestione
color_handlers = {
    "red": servers_red,
    "yellow": servers_yellow,
    "green": servers_green,
    "white": servers_white,
}


def hub_completion(t, servers, next_event_function):
    global hub_number

    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)

    if index is not None:

        response_time = t.current - servers[index].start_time
        stats.add_hub_response_time(response_time)

        servers[index].occupied = False
        servers[index].service_time = INF

        if servers == servers_hub:
            print(f"Job in hub completed at time {t.current}\n")
            color = assign_code()  # Assegna un colore
            t.color = color
            hub_number -= 1  # Decrementa il numero di job nel hub

            # Ottieni la lista dei server corretta in base al colore
            if color in color_handlers:
                next_event_function(t, color_handlers[color], color)

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


def next_event_function(t, servers, color):
    stream_map = {
        'red': stream_service_red,
        'yellow': stream_service_yellow,
        'green': stream_service_green,
        'white': stream_service_white
    }

    index = next((i for i, server in enumerate(servers) if not server.occupied), None)

    if index is not None:
        stream = stream_map[color]
        servers[index].service_time = t.current + get_service(stream, len(servers))
        servers[index].occupied = True
        servers[index].start_time = t.current  # Registra l'inizio del servizio

        # Aggiorna il tempo di completamento basato sul colore
        if color == 'red':
            t.red_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'yellow':
            t.yellow_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'green':
            t.green_completion = min(server.service_time for server in servers if server.occupied)
        elif color == 'white':
            t.white_completion = min(server.service_time for server in servers if server.occupied)
    else:
        # Se nessun server è libero, imposta il tempo di completamento all'infinito
        if color == 'red':
            t.red_completion = INF
        elif color == 'yellow':
            t.yellow_completion = INF
        elif color == 'green':
            t.green_completion = INF
        elif color == 'white':
            t.white_completion = INF


def run_simulation(stop_time):
    global hub_number, red_number, yellow_number, green_number, white_number
    t = Event(0, get_arrival(), INF, INF, INF, INF, INF)

    while t.current < stop_time:
        # Gestisci la situazione in cui tutti i tempi sono INF (nessun evento futuro)
        if all(x == INF for x in
               [t.arrival, t.hub_completion, t.red_completion, t.yellow_completion, t.green_completion,
                t.white_completion]):
            print("Simulation complete: no more events.")
            break

        print(f"Current time: {t.current}")
        print(
            f"Next events - Arrival: {t.arrival}, Hub completion: {t.hub_completion}, "
            f"Red completion: {t.red_completion}, "
            f"Yellow completion: {t.yellow_completion}, Green completion: {t.green_completion}, "
            f"White completion: {t.white_completion}")

        next_event_time = min(t.arrival, t.hub_completion, t.red_completion, t.yellow_completion, t.green_completion,
                              t.white_completion)

        t.current = next_event_time

        if t.current == t.arrival:
            process_arrival(t, servers_hub)
        elif t.current == t.hub_completion:
            hub_completion(t, servers_hub, next_event_function)
        elif t.current == t.red_completion:
            process_completion(t, servers_red, 'red')
        elif t.current == t.yellow_completion:
            process_completion(t, servers_yellow, 'yellow')
        elif t.current == t.green_completion:
            process_completion(t, servers_green, 'green')
        elif t.current == t.white_completion:
            process_completion(t, servers_white, 'white')


run_simulation(100)

# Stampa le statistiche finali
print(f"\nSYSTEM STATISTICS")
print(f"Total Jobs Completed: {stats.completed_jobs}")
print(f"Mean Response Time: {stats.mean_response_time()}")

print(f"\nHUB QUEUE STATISTICS")
print(f"Total hub Jobs Completed: {len(stats.hub_jobs_response_time)}")
print(f"Mean hub Response Time: {stats.get_hub_mean_response_time()}")
print(f"\n")
for response_time in stats.hub_jobs_response_time:
    print(f"{response_time}")

print(f"\nRED QUEUE STATISTICS")
print(f"Total Red Jobs Completed: {len(stats.red_jobs_response_time)}")
print(f"Mean Red Response Time: {stats.code_mean_response_time("red")}")
print(f"\n")
for response_time in stats.red_jobs_response_time:
    print(f"{response_time}")

print(f"\nYELLOW QUEUE STATISTICS")
print(f"Total yellow Jobs Completed: {len(stats.yellow_jobs_response_time)}")
print(f"Mean yellow Response Time: {stats.code_mean_response_time("yellow")}")
print(f"\n")
for response_time in stats.yellow_jobs_response_time:
    print(f"{response_time}")

print(f"\nGREEN QUEUE STATISTICS")
print(f"Total green Jobs Completed: {len(stats.green_jobs_response_time)}")
print(f"Mean green Response Time: {stats.code_mean_response_time("green")}")
print(f"\n")
for response_time in stats.green_jobs_response_time:
    print(f"{response_time}")

print(f"\nWHITE QUEUE STATISTICS")
print(f"Total white Jobs Completed: {len(stats.white_jobs_response_time)}")
print(f"Mean white Response Time: {stats.code_mean_response_time("white")}")
print(f"\n")
for response_time in stats.white_jobs_response_time:
    print(f"{response_time}")
