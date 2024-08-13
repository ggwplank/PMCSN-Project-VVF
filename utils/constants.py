INF = float('inf')

SERVERS_1 = 5  # Numero di serventi nel primo centro (Centralino/Hub)
SERVERS_2 = 3  # Numero di serventi nel secondo centro (Emergenza massima/Codice Rosso)
SERVERS_3 = 4  # Numero di serventi nel terzo centro (Emergenza alta/Codice Giallo)
SERVERS_4 = 3  # Numero di serventi nel quarto centro (Emergenza media/Codice Verde)
SERVERS_5 = 2  # Numero di serventi nel quinto centro (Emergenza bassa/Codice bianco)

MEAN_ARRIVAL_TIME = 5  # Tempo medio di arrivo

# Probabilità di assegnazione dei codici colore
CODE_ASSIGNMENT_PROBS = {
    "red": 25,
    "yellow": 50,
    "green": 75,
    "white": 100
}
