class Event:
    def __init__(self, current_time, arrival_time, hub_completion, red_completion, yellow_completion, green_completion,
                 color=None):
        self.current_time = current_time # tempo attuale dell'evento
        self.next_arrival = arrival_time # tempo del prossimo arrivo nel sistema
        self.color = color  # colore associato all'evento, se applicabile (tipo di richiesta)
        self.hub_completion = hub_completion    # tempo di completamento del prossimo job nel centralino
        self.red_completion = red_completion    # tempo di completamento del prossimo job in codice rosso
        self.yellow_completion = yellow_completion  # tempo di completamento del prossimo job in codice giallo
        self.green_completion = green_completion    # tempo di completamento del prossimo job in codice verde
