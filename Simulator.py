import random

INF = float('inf')
SERVERS_1 = 5  # Numero di serventi nella prima coda (Hub)
SERVERS_2 = 3  # Numero di serventi nella seconda coda (Codice Rosso)


class Server:
    def __init__(self):
        self.service_time = INF  # indica che non sta facendo nulla
        self.occupied = False
        self.color = None


class Event:
    def __init__(self, current_time, arrival_time, hub_completion, red_completion, color=None):
        self.current = current_time
        self.arrival = arrival_time
        self.hub_completion = hub_completion
        self.red_completion = red_completion
        self.color = color


# variabili di stato del sistema
servers_hub = [Server() for _ in range(SERVERS_1)]
servers_red = [Server() for _ in range(SERVERS_2)]

hub_number = 0
red_number = 0


# simulazione del tempo di arrivo
def get_arrival():
    return random.expovariate(1 / 5)  # Es: tempo medio tra arrivi = 5 minuti


# simulazione del tempo di servizio
def get_service(params):
    return random.expovariate(1 / params)  # Es: servizio medio


# assegnaizone del codice
def assign_code():
    return "red"


# processamento dell'arrivo nell'hub
def process_arrival(t, servers_hub):
    global hub_number
    print(f"Job arrived at time {t.current}")
    hub_number += 1
    t.arrival = get_arrival() + t.current

    index = next((i for i, server in enumerate(servers_hub) if not server.occupied), None)
    if index is not None:
        servers_hub[index].service_time = t.current + get_service(SERVERS_1)
        servers_hub[index].occupied = True
        t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
    else:
        t.hub_completion = INF  # Non ci sono servitori liberi


def process_completion(t, servers, next_event_function):
    global hub_number, red_number
    index = next((i for i, server in enumerate(servers) if server.service_time == t.current), None)
    if index is not None:
        servers[index].occupied = False
        servers[index].service_time = INF

        if servers == servers_hub:
            print(f"Job in hub completed at time {t.current}")
            color = assign_code()
            t.color = color
            hub_number -= 1  # Decrementa il numero di job nel hub
            next_event_function(t, servers_red)
            # Verifica se ci sono ancora server occupati prima di usare min()
            if any(server.occupied for server in servers_hub):
                t.hub_completion = min(server.service_time for server in servers_hub if server.occupied)
            else:
                t.hub_completion = INF
        else:
            print(f"Job in red completed at time {t.current}")
            red_number -= 1  # Decrementa il numero di job nel red
            if any(server.occupied for server in servers_red):
                t.red_completion = min(server.service_time for server in servers_red if server.occupied)
            else:
                t.red_completion = INF


def next_event_function(t, servers):
    index = next((i for i, server in enumerate(servers) if not server.occupied), None)
    if index is not None:
        servers[index].service_time = t.current + get_service(len(servers))
        servers[index].occupied = True
        t.red_completion = min(server.service_time for server in servers_red if server.occupied)
    else:
        t.red_completion = INF  # Non ci sono servitori liberi


def run_simulation(stop_time):
    global hub_number, red_number
    t = Event(0, get_arrival(), INF, INF)

    while t.current < stop_time:
        # Gestisci la situazione in cui tutti i tempi sono INF (nessun evento futuro)
        if all(x == INF for x in [t.arrival, t.hub_completion, t.red_completion]):
            print("Simulation complete: no more events.")
            break

        print(f"Current time: {t.current}")
        print(
            f"Next events - Arrival: {t.arrival}, Hub completion: {t.hub_completion}, Red completion: {t.red_completion}")

        next_event_time = min(t.arrival, t.hub_completion, t.red_completion)
        t.current = next_event_time

        if t.current == t.arrival:
            process_arrival(t, servers_hub)
        elif t.current == t.hub_completion:
            process_completion(t, servers_hub, next_event_function)
        elif t.current == t.red_completion:
            process_completion(t, servers_red, next_event_function)


run_simulation(50)
