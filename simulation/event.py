class Event:
    def __init__(self, current_time, arrival_time, hub_completion, red_completion, yellow_completion, green_completion,
                 white_completion, color=None):
        self.current = current_time # tempo attuale dell'evento #TODO current->current_time?
        self.arrival = arrival_time # tempo del prossimo arrivo nel sistema #TODO arrival->next_arrival?
        self.color = color  # colore associato all'evento, se applicabile (tipo di richiesta)
        self.hub_completion = hub_completion    # tempo di completamento del prossimo job nel centralino
        self.red_completion = red_completion    # tempo di completamento del prossimo job in emergenza massima
        self.yellow_completion = yellow_completion  # tempo di completamento del prossimo job in emergenza alta
        self.green_completion = green_completion    # tempo di completamento del prossimo job in emergenza media
        self.white_completion = white_completion    # tempo di completamento del prossimo job in emergenza bassa

#TODO perché è tutto del prossimo job? Ho sbagliato io a scrivere i commenti o erano già così?