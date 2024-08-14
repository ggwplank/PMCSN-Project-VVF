class Statistics:
    def __init__(self):
        self.total_response_time = 0.0  # tempo di risposta totale per tutti i job completati
        self.completed_jobs = 0  # numero di job completati

        # liste per i tempi di risposta per ogni tipologia di richiesta
        self.hub_jobs_response_times = []
        self.red_jobs_response_times = []
        self.yellow_jobs_response_times = []
        self.green_jobs_response_times = []
        self.white_jobs_response_times = []

    #TODO questo non è di sistema, ma dovrebbe essere rispetto a un singolo centro?
    def add_system_response_time(self, response_time):
        self.total_response_time += response_time
        self.completed_jobs += 1

    def mean_response_time(self):
        if self.completed_jobs > 0:
            return self.total_response_time / self.completed_jobs
        else:
            return 0.0

    def add_hub_response_time(self, response_time):
        """
        Registra il tempo di risposta di un job completato nell'hub.

        Parametri:
        - response_time (float): Tempo di risposta del job completato nell'hub.
        """
        self.hub_jobs_response_times.append(response_time)

    def get_hub_mean_response_time(self):
        """
        Calcola il tempo medio di risposta per i job completati nell'hub.

        Ritorna:
        - float: Il tempo medio di risposta per l'hub.
        """
        return evaluate_queue_mean_response_time(self.hub_jobs_response_times)

    def add_color_response_time(self, color, response_time):
        """
        Registra il tempo di risposta di un job completato in uno dei centri basati sul colore.

        Parametri:
        - color (str): Il colore del centro in cui il job è stato completato.
        - response_time (float): Tempo di risposta del job completato nel centro specificato.
        """
        if color == 'red':
            self.red_jobs_response_times.append(response_time)
        elif color == 'yellow':
            self.yellow_jobs_response_times.append(response_time)
        elif color == 'green':
            self.green_jobs_response_times.append(response_time)
        elif color == 'white':
            self.white_jobs_response_times.append(response_time)

    def code_mean_response_time(self, color):
        """
        Calcola il tempo medio di risposta per i job completati in uno specifico centro.

        Parametri:
        - color (str): Il colore del centro per cui calcolare il tempo medio di risposta.

        Ritorna:
        - float: Il tempo medio di risposta per il centro specificato.
        """
        if color == 'red':
            return evaluate_queue_mean_response_time(self.red_jobs_response_times)
        elif color == 'yellow':
            return evaluate_queue_mean_response_time(self.yellow_jobs_response_times)
        elif color == 'green':
            return evaluate_queue_mean_response_time(self.green_jobs_response_times)
        elif color == 'white':
            return evaluate_queue_mean_response_time(self.white_jobs_response_times)


def evaluate_queue_mean_response_time(jobs_response_time):
    """
    Calcola il tempo medio di risposta per una lista di tempi di risposta.

    Parametri:
    - jobs_response_time (list): Lista dei tempi di risposta per i job completati.

    Ritorna:
    - float: Il tempo medio di risposta per la lista fornita. Se la lista è vuota, ritorna 0.0.
    """
    code_mean_response_time = 0

    if len(jobs_response_time) > 0:
        for response_time in jobs_response_time:
            code_mean_response_time += response_time
        return code_mean_response_time / len(jobs_response_time)  # calcolo della media
    else:
        return 0.0  # ritorna 0 se non ci sono tempi di risposta registrati
