import matplotlib.pyplot as plt
import pandas as pd
import os
from utils.constants import FINITE_SIM_STATISTICS_FILENAME, INFINITE_SIM_STATISTICS_FILENAME, GRAPHS_OUTPUTS_DIR, SEED

def choose_horizon():
    choice = input("Vuoi generare grafici per orizzonte finito o infinito? (1/2): ").strip().lower()
    if choice == "1":
        return FINITE_SIM_STATISTICS_FILENAME, "finite_horizon"
    elif choice == "2":
        return INFINITE_SIM_STATISTICS_FILENAME, "infinite_horizon"
    else:
        print("Scelta non valida. Riprova.")
        return choose_horizon()

def plot_custom_graph(y_column, csv_file_path, x_column='Simulation', x_label='Simulation Run', y_label=None, sample_rate=16, save_dir='general'):
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
    plt.figure(figsize=(18, 9))  # Aumenta la larghezza per migliorare la leggibilità
    plt.plot(sampled_x_values, sampled_y_values, linestyle='-', color='#1f77b4', linewidth=2, markersize=6, label=y_label)

    # Etichette degli assi
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    plt.title(f'{y_column} per {x_label} \n Seed: {SEED}', fontsize=20, fontweight='bold', pad=20)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=14, loc='best')
    # Aggiungi un bordo attorno al grafico
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.tight_layout(pad=2)
    output_dir = os.path.join(GRAPHS_OUTPUTS_DIR, save_dir)

    # Creazione della cartella solo se non esiste
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        print(f"Creata la cartella: {save_dir}")

    output_filename = f'{y_column}.png'
    output_file_path = os.path.join(save_dir, output_filename)

    try:
        plt.savefig(output_file_path, dpi=300, bbox_inches='tight')
        print(f"Grafico salvato in: {output_file_path}")
    except Exception as e:
        print(f"Errore durante il salvataggio del grafico: {e}")
    plt.close()

def generate_all_graphs_by_category():
    csv_filename, horizon_folder = choose_horizon()
    csv_file_path = "../" + csv_filename
    # Carica i dati dal file CSV
    data = pd.read_csv(csv_file_path)
    horizon_output_dir = os.path.join(GRAPHS_OUTPUTS_DIR, horizon_folder)
    categories = {
        "red_queue": [],
        "green_queue": [],
        "yellow_queue": [],
        "hub": [],
        "general": []
    }

    # Categorizza le colonne in base al nome
    for column in data.columns:
        if 'red' in column.lower():
            categories["red_queue"].append(column)
        elif 'green' in column.lower():
            categories["green_queue"].append(column)
        elif 'yellow' in column.lower():
            categories["yellow_queue"].append(column)
        elif 'hub' in column.lower():
            categories["hub"].append(column)
        else:
            categories["general"].append(column)

    for category, columns in categories.items():
        for column in columns:
            if column != 'Simulation':
                print(f"Generazione del grafico per la colonna: {column} nella categoria: {category}")
                plot_custom_graph(y_column=column, csv_file_path=csv_file_path, save_dir=os.path.join(horizon_output_dir, category))


generate_all_graphs_by_category()
