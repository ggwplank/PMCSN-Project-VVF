INF = float('inf')

HUB_SERVERS = 5  # Numero di serventi nel primo centro (Centro operativo)
OPERATIVE_SERVERS = 2  #

MEAN_ARRIVAL_TIME = 2  # Tempo medio di arrivo
MEAN_HUB_SERVICE_TIME = 3  # Tempo medio di servizio nell' hub

#
SQUADRA = "squadra"
MODULO = "modulo"

# Probabilità di assegnazione dei codici colore
CODE_ASSIGNMENT_PROBS = {
    "red": 10,
    "yellow": 30,
    "green": 100
}

# Probabilità di autorisoluzione dei job in coda
AUTORESOLUTION_GREEN_PROB = 15
AUTORESOLUTION_YELLOW_PROB = 3
