import matplotlib.pyplot as plt
import pandas as pd
import os

from utils.constants import FINITE_SIM_STATISTICS_FILENAME, GRAPHS_OUTPUTS_DIR


# Funzione generica per disegnare grafici
def plot_custom_graph(y_column, x_column='Simulation', x_label='Simulation Run', y_label=None, sample_rate=16):
    # Percorso del file CSV fisso
    csv_file_path = "../" + FINITE_SIM_STATISTICS_FILENAME

    # Carica i dati dal file CSV
    data = pd.read_csv(csv_file_path)

    # Verifica se le colonne esistono nel CSV
    if x_column not in data.columns or y_column not in data.columns:
        raise ValueError(f"Colonne '{x_column}' o '{y_column}' non trovate nel CSV.")

    # Estrae le colonne necessarie per il grafico
    x_values = data[x_column]
    y_values = data[y_column]

    # Se y_label non è specificato, usa il nome della colonna y_column
    if y_label is None:
        y_label = y_column

    # Campionamento dei dati per migliorare la leggibilità del grafico
    sampled_x_values = x_values[::sample_rate]
    sampled_y_values = y_values[::sample_rate]

    # Creazione del grafico
    plt.figure(figsize=(16, 8))
    plt.plot(sampled_x_values, sampled_y_values, linestyle='-', color='b')
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.title(f'{y_column} per {x_label}', fontsize=16, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Verifica se la cartella OUTPUTS_DIR esiste, altrimenti la crea
    if not os.path.exists(GRAPHS_OUTPUTS_DIR):
        os.makedirs(GRAPHS_OUTPUTS_DIR)
        print(f"Creata la cartella: {GRAPHS_OUTPUTS_DIR}")


    # Salva il grafico come file PNG
    output_filename = f'{y_column}.png'
    output_file_path = os.path.join(GRAPHS_OUTPUTS_DIR, output_filename)
    plt.savefig(output_file_path, dpi=300)
    plt.show()

    print(f"Grafico salvato in: {output_file_path}")


plot_custom_graph(
    y_column='mean_service_green_time',
)
