import csv

# Dati raccolti
data = {
    "CODICE ROSSO": {
        "Acqua": {"Durata Media (minuti)": 44.6, "Durata Complessiva (ore)": 2357.5, "Numero Interventi": 3171},
        "Gas": {"Durata Media (minuti)": 47.1, "Durata Complessiva (ore)": 2820.3, "Numero Interventi": 3595},
        "Incendi ed esplosioni": {"Durata Media (minuti)": 57.6, "Durata Complessiva (ore)": 19519.9,
                                  "Numero Interventi": 20329},
        "Incidenti stradali": {"Durata Media (minuti)": 46.6, "Durata Complessiva (ore)": 3132.2,
                               "Numero Interventi": 4037},
        "Soccorso a persona": {"Durata Media (minuti)": 39.1, "Durata Complessiva (ore)": 7446.7,
                               "Numero Interventi": 11421},
        "Statica": {"Durata Media (minuti)": 41.2, "Durata Complessiva (ore)": 4094.0, "Numero Interventi": 5965},
        "Totale": {"Durata Media (minuti)": 276.2, "Durata Complessiva (ore)": 39370.6, "Numero Interventi": 48518},
        "Probabilità": 0.6009,
        "Numero di ore per caserma all’anno": 803.4816,
        "Tempo in minuti per risolvere": 46.0333
    },
    "CODICE GIALLO": {
        "Attività di polizia giudiziaria": {"Durata Media (minuti)": 162.3, "Durata Complessiva (ore)": 408.5,
                                            "Numero Interventi": 151},
        "Recuperi": {"Durata Media (minuti)": 54.3, "Durata Complessiva (ore)": 1126.5, "Numero Interventi": 1245},
        "Alberi pericolanti": {"Durata Media (minuti)": 41.7, "Durata Complessiva (ore)": 4989.1,
                               "Numero Interventi": 7170},
        "Ascensori bloccati": {"Durata Media (minuti)": 15.7, "Durata Complessiva (ore)": 1041.1,
                               "Numero Interventi": 3984},
        "Totale": {"Durata Media (minuti)": 274.0, "Durata Complessiva (ore)": 7565.2, "Numero Interventi": 12550},
        "Probabilità": 0.2078,
        "Numero di ore per caserma all’anno": 154.3918,
        "Tempo in minuti per risolvere": 68.5
    },
    "CODICE VERDE": {
        "Aeromobili": {"Durata Media (minuti)": 76.5, "Durata Complessiva (ore)": 90.5, "Numero Interventi": 71},
        "Aperture porte e finestre": {"Durata Media (minuti)": 19.6, "Durata Complessiva (ore)": 3455.2,
                                      "Numero Interventi": 10558},
        "Bonifica da insetti": {"Durata Media (minuti)": 32.8, "Durata Complessiva (ore)": 1905.2,
                                "Numero Interventi": 3484},
        "Porti": {"Durata Media (minuti)": 148.3, "Durata Complessiva (ore)": 279.2, "Numero Interventi": 113},
        "Salvataggio animali": {"Durata Media (minuti)": 38.1, "Durata Complessiva (ore)": 777.0,
                                "Numero Interventi": 1223},
        "Totale": {"Durata Media (minuti)": 315.8, "Durata Complessiva (ore)": 6507.1, "Numero Interventi": 15449},
        "Probabilità": 0.1913,
        "Numero di ore per caserma all’anno": 132.7979,
        "Tempo in minuti per risolvere": 63.16
    },
    "FALSO ALLARME": {
        "Falso allarme": {"Durata Media (minuti)": 16.9, "Durata Complessiva (ore)": 154.4, "Numero Interventi": 548},
        "Probabilità di ricevere servizio nullo": 0.0060
    },
    "INTERVENTI NON PIÙ NECESSARI": {
        "Interventi non più necessario": {"Durata Media (minuti)": 11.9, "Durata Complessiva (ore)": 1832.3,
                                          "Numero Interventi": 9221},
        "Probabilità di autorisoluzione": 0.10188
    }
}

# Header del CSV
header = ["Codice", "Tipo di Intervento", "Durata Media (minuti)", "Durata Complessiva (ore)", "Numero Interventi",
          "Probabilità", "Numero di ore per caserma all’anno", "Tempo in minuti per risolvere"]

# Creazione del file CSV
filename = "Interventi_VVF_Lazio.csv"
with open(filename, "w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)

    # Scrivi l'intestazione
    writer.writeheader()

    # Scrivi i dati per ogni codice di intervento
    for codice, interventi in data.items():
        # Estrai i valori comuni a tutti i tipi di intervento per quel codice
        probabilita = interventi.get("Probabilità", "")
        ore_per_caserma = interventi.get("Numero di ore per caserma all’anno", "")
        tempo_per_risolvere = interventi.get("Tempo in minuti per risolvere", "")

        for tipo, dettagli in interventi.items():
            # Controlla se "dettagli" è un dizionario o un valore singolo
            if isinstance(dettagli, dict):
                row = {
                    "Codice": codice,
                    "Tipo di Intervento": tipo,
                    "Durata Media (minuti)": dettagli.get("Durata Media (minuti)", ""),
                    "Durata Complessiva (ore)": dettagli.get("Durata Complessiva (ore)", ""),
                    "Numero Interventi": dettagli.get("Numero Interventi", ""),
                    "Probabilità": probabilita,
                    "Numero di ore per caserma all’anno": ore_per_caserma,
                    "Tempo in minuti per risolvere": tempo_per_risolvere
                }
                writer.writerow(row)

print(f"File CSV '{filename}' creato con successo.")
