INF = float('inf')

HUB_SERVERS = 5  # Numero di serventi nel primo centro (Centro operativo)
OPERATIVE_SERVERS = 2  #

MEAN_ARRIVAL_TIME = 1  # Tempo medio di arrivo
MEAN_HUB_SERVICE_TIME = 0.3  # Tempo medio di servizio nell' hub
MEAN_RED_SERVICE_TIME = 0.0005
MEAN_YELLOW_SERVICE_TIME = 0.005
MEAN_GREEN_SERVICE_TIME = 0.05

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

# seed
SEED = 324516786
B = 1080  # size del batch in termini di job
K = 96  # numero di batch utilizzati
REPLICATIONS = 96  # deve essere <= di K in quanto la stampa delle replicazioni si basa su quella dei batch

