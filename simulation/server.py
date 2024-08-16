from utils.constants import INF


class Server:
    def __init__(self):
        self.end_service_time = INF  # il server non sta facendo nulla
        self.occupied = False  # flag che indica se il server è attualmente occupato
        self.type = None  # Tipo di server (Squadra o Modulo)
        self.job_color = None # Classe del job a cui è assegnato questo server
        self.start_service_time = None  # per tracciare l'inizio del servizio
