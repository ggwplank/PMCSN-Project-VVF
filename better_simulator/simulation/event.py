class Event:
    def __init__(self, current_time, next_arrival, hub_completion, red_completion, orange_completion, yellow_completion_squadra, yellow_completion_modulo,
                     green_completion_modulo):
        self.current_time = current_time  # Tempo corrente della simulazione
        self.next_arrival = next_arrival  # Tempo del prossimo arrivo
        self.hub_completion = hub_completion  # Tempo completamento del prossimo job nell'hub
        self.red_completion = red_completion  # Tempo completamento del prossimo job red
        self.orange_completion = orange_completion  # Tempo completamento del prossimo job arancione
        self.yellow_completion_squadra = yellow_completion_squadra  # Tempo completamento del prossimo job yellow (squadra)
        self.yellow_completion_modulo = yellow_completion_modulo # Tempo completamento del prossimo job yellow (modulo)
        self.green_completion_modulo = green_completion_modulo  # Tempo completamento del prossimo job green (modulo)
