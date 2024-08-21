# Importazioni standard
INF = float('inf')

# ---------------------------------
# COSTANTI RELATIVE AI SERVER
# ---------------------------------

HUB_SERVERS = 2  # Numero di serventi nel centro operativo (Hub)
OPERATIVE_SERVERS = 2  # Numero di serventi nel centro operativo (altro tipo)

# ---------------------------------
# TEMPI MEDI (ARRIVI E SERVIZI)
# ---------------------------------

MEAN_ARRIVAL_TIME = 116.23  # Tempo medio di arrivo dei job al minuto
MEAN_HUB_SERVICE_TIME = 1.5  # Tempo medio di servizio nell'Hub al minuto
MEAN_RED_SERVICE_TIME = 61.033333  # Tempo medio di servizio per i job con codice rosso
MEAN_YELLOW_SERVICE_TIME = 90.4777  # Tempo medio di servizio per i job con codice giallo
MEAN_GREEN_SERVICE_TIME = 175  # Tempo medio di servizio per i job con codice verde

# ---------------------------------
# PROBABILITÀ DI ASSEGNAZIONE E AUTORISOLUZIONE
# ---------------------------------

# Probabilità di assegnazione dei codici colore
CODE_ASSIGNMENT_PROBS = {
    "red": 51.48,
    "yellow": 81.19,  # 51.48 + 29.71
    "green": 100
}

# Probabilità di autorisoluzione dei job in coda
AUTORESOLUTION_RED_PROB = 4.56    # Codice rosso # TODO implementa la red autoresolution
AUTORESOLUTION_YELLOW_PROB = 2.63  # Codice giallo
AUTORESOLUTION_GREEN_PROB = 1.67   # Codice verde

# TODO implementa il fake allarm
FAKE_ALLARM_RED_PROB = 0.27
FAKE_ALLARM_YELLOW_PROB = 0.15
FAKE_ALLARM_GREEN_PROB = 0.09

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
