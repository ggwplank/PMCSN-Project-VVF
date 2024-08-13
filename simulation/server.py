from utils.constants import INF


class Server:
    def __init__(self):
        self.service_time = INF  # il server non sta facendo nulla
        self.occupied = False  # flag che indica se il server è attualmente occupato
        self.color = None  # colore associato al server
        self.start_time = None  # per tracciare l'inizio del servizio
