INF = float('inf')

SERVERS_1 = 5  # Numero di serventi nel primo centro (Centralino/Hub)
SERVERS_2 = 3  # Numero di serventi nel secondo centro (Emergenza alta/Codice Rosso)
SERVERS_3 = 4  # Numero di serventi nel terzo centro (Emergenza media/Codice Giallo)
SERVERS_4 = 3  # Numero di serventi nel quarto centro (Emergenza bassa/Codice Verde)

MEAN_ARRIVAL_TIME = 5  # Tempo medio di arrivo

# Probabilità di assegnazione dei codici colore
CODE_ASSIGNMENT_PROBS = {
    "red": 33,
    "yellow": 67,
    "green": 10
}
