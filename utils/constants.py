# Importazioni standard
INF = float('inf')

# ---------------------------------
# COSTANTI RELATIVE AI SERVER
# ---------------------------------

HUB_SERVERS = 5  # Numero di serventi nel centro operativo (Hub)
OPERATIVE_SERVERS = 2  # Numero di serventi nel centro operativo (altro tipo)

# ---------------------------------
# TEMPI MEDI (ARRIVI E SERVIZI)
# ---------------------------------

MEAN_ARRIVAL_TIME = 2  # Tempo medio di arrivo dei job
MEAN_HUB_SERVICE_TIME = 5  # Tempo medio di servizio nell'Hub
MEAN_RED_SERVICE_TIME = 0.005  # Tempo medio di servizio per i job con codice rosso
MEAN_YELLOW_SERVICE_TIME = 0.05  # Tempo medio di servizio per i job con codice giallo
MEAN_GREEN_SERVICE_TIME = 0.5  # Tempo medio di servizio per i job con codice verde

# ---------------------------------
# PROBABILITÀ DI ASSEGNAZIONE E AUTORISOLUZIONE
# ---------------------------------

# Probabilità di assegnazione dei codici colore
CODE_ASSIGNMENT_PROBS = {
    "red": 10,
    "yellow": 30,
    "green": 100
}

# Probabilità di autorisoluzione dei job in coda
AUTORESOLUTION_GREEN_PROB = 15  # Codice verde
AUTORESOLUTION_YELLOW_PROB = 3  # Codice giallo

# ---------------------------------
# COSTANTI GENERALI DEL SISTEMA
# ---------------------------------

SQUADRA = "squadra"  # Nome della squadra (label usata nel sistema)
MODULO = "modulo"  # Nome del modulo (label usata nel sistema)

SEED = 324516786  # Seed per la generazione casuale

# ---------------------------------
# STATISTICHE E ANALISI
# ---------------------------------

LOC = 0.95  # Livello di confidenza (Level of Confidence) per intervalli
ALPHA = 0.05  # Livello di significatività (1 - LOC)

B = 1080  # Dimensione del batch in termini di job
K = 96  # Numero di batch utilizzati
REPLICATIONS = 96  # Numero di replicazioni (deve essere <= K)

# ---------------------------------
# FILES E PATHS
# ---------------------------------

TEMP_FILENAME = "temp_file.csv"  # Nome del file temporaneo
REPORT_FILENAME = "SimulationReport.txt"  # Nome del file di report finale
