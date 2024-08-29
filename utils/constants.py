# Importazioni standard
import os

INF = float('inf')

# ---------------------------------
# COSTANTI RELATIVE AI SERVER
# ---------------------------------

HUB_SERVERS = 2  # Numero di serventi nel centro operativo (Hub)
OPERATIVE_SERVERS = 2  # Numero di serventi nel centro operativo (altro tipo)

# ---------------------------------
# TEMPI MEDI (ARRIVI E SERVIZI)
# ---------------------------------

MEAN_ARRIVAL_TIME = 116.23  # Tempo medio di arrivo dei job [min/job]
MEAN_HUB_SERVICE_TIME = 1.5  # Tempo medio di servizio E[s] in un servente dell'hub [min/job]
MEAN_RED_SERVICE_TIME = 61.033333  # Tempo medio di servizio E[s] per i job con codice rosso [min/job]
MEAN_YELLOW_SERVICE_TIME = 90.47777778  # Tempo medio di servizio E[s] per i job con codice giallo [min/job]
MEAN_GREEN_SERVICE_TIME = 175  # Tempo medio di servizio per E[s] i job con codice verde [min/job]

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
AUTORESOLUTION_RED_PROB = 0  # Codice rosso (4.56)
AUTORESOLUTION_YELLOW_PROB = 0  # Codice giallo (2.63)
AUTORESOLUTION_GREEN_PROB = 0  # Codice verde (1.67)

FAKE_ALLARM_RED_PROB = 0  # 0.27
FAKE_ALLARM_YELLOW_PROB = 0  # 0.15
FAKE_ALLARM_GREEN_PROB = 0  # 0.09

# ---------------------------------
# COSTANTI GENERALI DEL SISTEMA
# ---------------------------------

SQUADRA = "squadra"  # Nome della squadra (label usata nel sistema)
MODULO = "modulo"  # Nome del modulo (label usata nel sistema)

# Seeds per la generazione casuale
seeds = {
    "1": 324516786,
    "2": 140620017,
    "3": 170920015,
    "4": 170520018,
    "5": 240619974
}
SEED = seeds["1"]
SEED_INDEX = list(seeds.keys())[list(seeds.values()).index(SEED)]


# ---------------------------------
# STATISTICHE E ANALISI
# ---------------------------------

LOC = 0.95  # Livello di confidenza (Level of Confidence) per intervalli
ALPHA = 0.05  # Livello di significatività (1 - LOC)

INTERVAL = 1440 * 7  # Intervallo di analisi per ogni run espresso in minuti

B = 512  # Dimensione del batch in termini di job
K = 1024  # Numero di batch utilizzati

REPLICATIONS = 1024  # Numero di replicazioni (deve essere <= K)

INFINITE = 0
FINITE = 1
SIMULATION_TYPE = FINITE

# ---------------------------------
# FILES E PATHS
# ---------------------------------

REPORTS_OUTPUTS_DIR = os.path.join("outputs", "reports")
STATISTICS_OUTPUTS_DIR = os.path.join("outputs", "statistics")

FINITE_SIM_REPORT_FILENAME = os.path.join(REPORTS_OUTPUTS_DIR, "finite-sim-report-" + SEED_INDEX + ".txt")
INFINITE_SIM_REPORT_FILENAME = os.path.join(REPORTS_OUTPUTS_DIR, "infinite-sim-report-" + SEED_INDEX + ".txt")

FINITE_SIM_STATISTICS_FILENAME = os.path.join(STATISTICS_OUTPUTS_DIR, "finite-statistics-" + SEED_INDEX + ".csv")
INFINITE_SIM_STATISTICS_FILENAME = os.path.join(STATISTICS_OUTPUTS_DIR, "infinite-statistics-" + SEED_INDEX + ".csv")

GRAPHS_OUTPUTS_DIR = os.path.join("../outputs", "graphs")
