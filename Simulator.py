import random

INF = float('inf')
SERVERS_1 = 5  # Numero di serventi nella prima coda (Hub)
SERVERS_2 = 3  # Numero di serventi nella seconda coda (Codice Rosso)
SERVERS_3 = 4
SERVERS_4 = 3
SERVERS_5 = 2


class Server:
    def __init__(self):
        self.service_time = INF  # indica che non sta facendo nulla
        self.occupied = False
        self.color = None


class Event:
    def __init__(self, current_time, arrival_time, hub_completion, red_completion, yellow_completion, green_completion,
                 white_completion, color=None):
        self.current = current_time
        self.arrival = arrival_time
        self.color = color
        self.hub_completion = hub_completion
        self.red_completion = red_completion
        self.yellow_completion = yellow_completion
        self.green_completion = green_completion
        self.white_completion = white_completion


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
    return random.expovariate(1 / 5)  # Es: tempo medio tra arrivi = 5 minuti


# Simulazione del tempo di servizio
def get_service(params):
    return random.expovariate(1 / params)  # Es: servizio medio


# Assegnazione del codice
def assign_code():
    p = random.uniform(0, 100)
    if p < 25:
        return "red"
    elif p < 50:
        return "yellow"
    elif p < 75:
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
        servers_hub[index].service_time = t.current + get_service(SERVERS_1)
        servers_hub[index].occupied = True
        t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF  # Non ci sono servitori liberi


def process_red(t, servers_red):
    global red_number
    print(f"Completed red job at time {t.current}\n")
    red_number -= 1  # Decrementa il numero di job nel red
    index = next((i for i, server in enumerate(servers_red) if server.service_time == t.current), None)
    if index is not None:
        servers_red[index].occupied = False
        servers_red[index].service_time = INF

    if any(server.occupied for server in servers_red):
        t.red_completion = min(server.service_time for server in servers_red if server.occupied)
    else:
        t.red_completion = INF


def process_yellow(t, servers_yellow):
    global yellow_number
    print(f"Completed yellow job at time {t.current}\n")
    yellow_number -= 1  # Decrementa il numero di job nel white
    index = next((i for i, server in enumerate(servers_yellow) if server.service_time == t.current), None)
    if index is not None:
        servers_yellow[index].occupied = False
        servers_yellow[index].service_time = INF

    if any(server.occupied for server in servers_yellow):
        t.yellow_completion = min(server.service_time for server in servers_yellow if server.occupied)
    else:
        t.yellow_completion = INF


def process_green(t, servers_green):
    global green_number
    print(f"Completed green job at time {t.current}\n")
    green_number -= 1  # Decrementa il numero di job nel white
    index = next((i for i, server in enumerate(servers_green) if server.service_time == t.current), None)
    if index is not None:
        servers_green[index].occupied = False
        servers_green[index].service_time = INF

    if any(server.occupied for server in servers_green):
        t.green_completion = min(server.service_time for server in servers_green if server.occupied)
    else:
        t.green_completion = INF


def process_white(t, servers_white):
    global white_number
    print(f"Completed white job at time {t.current}\n")
    white_number -= 1  # Decrementa il numero di job nel white
    index = next((i for i, server in enumerate(servers_white) if server.service_time == t.current), None)
    if index is not None:
        servers_white[index].occupied = False
        servers_white[index].service_time = INF

    if any(server.occupied for server in servers_white):
        t.white_completion = min(server.service_time for server in servers_white if server.occupied)
    else:
        t.white_completion = INF


# Dizionario che mappa i colori alle funzioni di gestione
color_handlers = {
    "red": process_red,
    "yellow": process_yellow,
    "green": process_green,
    "white": process_white,

}

# Mappatura tra colori e server
color_to_servers = {
    'red': servers_red,
    'yellow': servers_yellow,
    'green': servers_green,
    'white': servers_white,
}


def hub_completion(t, servers, next_event_function):
    global hub_number

    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)

    if index is not None:
        servers[index].occupied = False
        servers[index].service_time = INF

        if servers == servers_hub:
            print(f"Job in hub completed at time {t.current}\n")
            color = assign_code()  # Assegna un colore
            t.color = color
            hub_number -= 1  # Decrementa il numero di job nel hub

            # Ottieni la lista dei server corretta in base al colore
            if color in color_to_servers:
                next_event_function(t, color_to_servers[color], color)

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
    index = next((i for i, server in enumerate(servers) if not server.occupied), None)

    if index is not None:
        servers[index].service_time = t.current + get_service(len(servers))
        servers[index].occupied = True

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
            process_red(t, servers_red)  # Chiama direttamente la funzione di completamento red
        elif t.current == t.yellow_completion:
            process_yellow(t, servers_yellow)  # Chiama direttamente la funzione di completamento yellow
        elif t.current == t.green_completion:
            process_green(t, servers_green)  # Chiama direttamente la funzione di completamento green
        elif t.current == t.white_completion:
            process_white(t, servers_white)  # Chiama direttamente la funzione di completamento white



run_simulation(100)
