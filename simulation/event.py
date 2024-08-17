class Event:
    def __init__(self, current_time, next_arrival, hub_completion, red_completion, yellow_completion, green_completion_squadra, green_completion_modulo):
        self.current_time = current_time  # Tempo corrente della simulazione
        self.next_arrival = next_arrival  # Tempo del prossimo arrivo
        self.hub_completion = hub_completion  # Tempo di completamento del prossimo job nell'hub
        self.red_completion = red_completion  # Tempo di completamento del prossimo job red
        self.yellow_completion = yellow_completion  # Tempo di completamento del prossimo job yellow
        self.green_completion_squadra = green_completion_squadra  # Tempo di completamento del prossimo job green gestito dalla squadra
        self.green_completion_modulo = green_completion_modulo  # Tempo di completamento del prossimo job green gestito dal modulo
