import matplotlib.pyplot as plt
import pandas as pd
import os
from simulator.utils.constants import  seeds

FIGSIZE = (18, 9)
DPI = 300
MARKERSIZE = 6
XTICK_ROTATION = 45
FONTSIZE_TITLE = 20
FONTSIZE_LABELS = 16
FONTSIZE_LEGEND = 14
FONTSIZE_TICKS = 12

STATISTICS_OUTPUTS_DIR = os.path.join("..","outputs", "statistics")
GRAPHS_OUTPUTS_DIR = os.path.join("../outputs", "graphs")

COLUMNS_TO_PLOT = [
    "mean_queue_hub_time", "mean_queue_red_time", "mean_queue_yellow_time", "mean_queue_green_squadra_time","mean_queue_green_modulo_time",
    "mean_N_queue_hub", "mean_N_queue_red", "mean_N_queue_yellow", "mean_N_queue_green_squadra", "mean_N_queue_green_modulo",
]

COLORS = ['b', 'g', 'r', 'c', 'm']  # Blu, Verde, Rosso, Ciano, Magenta


def choose_horizon():
    choice = input("Vuoi generare grafici per orizzonte finito (1) o infinito (2)? ").strip().lower()
    print("\n")
    if choice == "1":
        return "finite_horizon", "finite-statistics"
    elif choice == "2":
        return "infinite_horizon", "infinite-statistics"
    else:
        print("Scelta non valida. Riprova.")
        return choose_horizon()

def plot_custom_graphs_across_seeds(csv_paths, y_column, save_dir, sample_rate=16):
    plt.figure(figsize=FIGSIZE)

    for i, (seed_key, csv_path) in enumerate(csv_paths.items()):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File CSV non trovato: {csv_path}")

        data = pd.read_csv(csv_path)

        # Verifica se la colonna esiste nel CSV
        if y_column not in data.columns:
            raise ValueError(f"Colonna '{y_column}' non trovata nel CSV per il seed {seed_key}.")

        x_values = data['Simulation'][::sample_rate]
        y_values = data[y_column][::sample_rate]

        '''  
             # Solo i marker, senza linee
             plt.plot(x_values, y_values, linestyle='', markersize=MARKERSIZE,
                      color=COLORS[i], marker='o', label=f'Seed: {seeds[seed_key]}')
             '''
        plt.plot(x_values, y_values, linestyle='-', linewidth='2', markersize=MARKERSIZE,
                 color=COLORS[i], marker='o', label=f'Seed: {seeds[seed_key]}')

    plt.xlabel('Simulation Run', fontsize=FONTSIZE_LABELS)
    plt.ylabel(y_column, fontsize=FONTSIZE_LABELS)
    plt.title(f'{y_column} per Simulation Run', fontsize=FONTSIZE_TITLE, fontweight='bold', pad=20)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xticks(rotation=XTICK_ROTATION, fontsize=FONTSIZE_TICKS)
    plt.yticks(fontsize=FONTSIZE_TICKS)

    # Posizionamento della legenda fuori dal grafico
    plt.legend(fontsize=FONTSIZE_LEGEND, loc='upper left', bbox_to_anchor=(1, 1))

    # aggiugiamo il bordo attorno al grafico
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.tight_layout(pad=2)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        print(f"Creata la cartella: {save_dir}\n")

    output_filename = f'{y_column}_comparison.png'
    output_file_path = os.path.join(save_dir, output_filename)

    try:
        plt.savefig(output_file_path, dpi=DPI, bbox_inches='tight')
        print(f"Grafico salvato in: {output_file_path}\n")
    except Exception as e:
        print(f"Errore durante il salvataggio del grafico: {e}")
    plt.close()

def generate_comparison_graphs(sample_rate=16):
    horizon_choice, file_prefix = choose_horizon()

    csv_paths = {seed_key: os.path.join(STATISTICS_OUTPUTS_DIR, f"{file_prefix}-{seed_key}.csv") for seed_key in seeds.keys()}
    sample_csv_path = next(iter(csv_paths.values()))  # Prende il percorso del primo CSV per ottenere le colonne

    if not os.path.exists(sample_csv_path):
        raise FileNotFoundError(f"File CSV non trovato: {sample_csv_path}")

    data = pd.read_csv(sample_csv_path)
    horizon_output_dir = os.path.join(GRAPHS_OUTPUTS_DIR, horizon_choice)

    for column in COLUMNS_TO_PLOT:
        if column in data.columns:
            print(f"Generazione del grafico comparativo per la colonna: {column}")
            plot_custom_graphs_across_seeds(csv_paths, y_column=column, save_dir=horizon_output_dir,
                                            sample_rate=sample_rate)
        else:
            print(f"Colonna {column} non trovata nei file CSV.")

generate_comparison_graphs(sample_rate=75)