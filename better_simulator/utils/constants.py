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
MEAN_RED_SERVICE_TIME = 71.033333 - 25  # Tempo medio di servizio E[s] per i job con codice rosso [min/job]
MEAN_ORANGE_SERVICE_TIME = 56.925 - 25  # Tempo medio di servizio E[s] per i job con codice arancione [min/job]
MEAN_YELLOW_SERVICE_TIME = 117.32 - 25  # Tempo medio di servizio E[s] per i job con codice giallo [min/job]
MEAN_GREEN_SERVICE_TIME = 175 - 25  # Tempo medio di servizio per E[s] i job con codice verde [min/job]

# ---------------------------------
# PROBABILITÀ DI ASSEGNAZIONE E AUTORISOLUZIONE
# ---------------------------------

# Probabilità di assegnazione dei codici colore
CODE_ASSIGNMENT_PROBS = {
    "red": 51.48,
    "orange": 51.48 + 18.05,  # 51.48 + 18.05
    "yellow": 69.53 + 11.66,  # 69.53 + 11.66
    "green": 100
}

FAKE_ALLARM_RED_PROB = 0.27  # 0.27
FAKE_ALLARM_ORANGE_PROB = 0.09  # 0.09
FAKE_ALLARM_YELLOW_PROB = 0.06  # 0.06
FAKE_ALLARM_GREEN_PROB = 0.1  # 0.1

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
SEED = seeds[("5")]
SEED_INDEX = list(seeds.keys())[list(seeds.values()).index(SEED)]

# ---------------------------------
# STATISTICHE E ANALISI
# ---------------------------------

LOC = 0.95  # Livello di confidenza (Level of Confidence) per intervalli
ALPHA = 0.05  # Livello di significatività (1 - LOC)

INTERVAL = 1440 * 7  # Intervallo di analisi per ogni run espresso in minuti

B = 1096  # Dimensione del batch in termini di job
K = 260  # Numero di batch utilizzati

REPLICATIONS = 260  # Numero di replicazioni (deve essere <= K)

INFINITE = 0
FINITE = 1
SIMULATION_TYPE = INFINITE

# ---------------------------------
# FILES E PATHS
# ---------------------------------

REPORTS_OUTPUTS_DIR = os.path.join("outputs", "reports")
STATISTICS_OUTPUTS_DIR = os.path.join("outputs", "statistics")

FINITE_SIM_REPORT_FILENAME = os.path.join(REPORTS_OUTPUTS_DIR, "finite-sim-report-" + SEED_INDEX + ".txt")
INFINITE_SIM_REPORT_FILENAME = os.path.join(REPORTS_OUTPUTS_DIR,
                                            "FA-infinite-sim-report-" + SEED_INDEX + ".txt")

FINITE_SIM_STATISTICS_FILENAME = os.path.join(STATISTICS_OUTPUTS_DIR, "finite-statistics-" + SEED_INDEX + ".csv")
INFINITE_SIM_STATISTICS_FILENAME = os.path.join(STATISTICS_OUTPUTS_DIR,
                                                "FA-infinite-statistics-" + SEED_INDEX + ".csv")

GRAPHS_OUTPUTS_DIR = os.path.join("../better_simulator/outputs", "graphs")
