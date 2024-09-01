import matplotlib.pyplot as plt
import pandas as pd
import os
from standard_simulator.utils.constants import seeds

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

color_translation = {
    "red": "Rossa",
    "yellow": "Gialla",
    "green": "Verde",
    "green_squadra": "Squadra Verde",
    "green_modulo": "Modulo Verde",
    "hub": "Hub"
}

def choose_graph_type():
    choice = input("Vuoi generare grafici a linea (1) o a colonna (2) o comparare i seed (3)? ").strip().lower()
    if choice == "1":
        return "line"
    elif choice == "2":
        return "bar"
    elif choice == "3":
        return "multiple"
    else:
        print("Scelta non valida. Riprova.")
        return choose_graph_type()

def choose_horizon():
    choice = input("Vuoi generare grafici per orizzonte finito (1) o infinito (2)? ").strip().lower()
    print("\n")
    if choice == "1":
        return "finite_horizon", "finite-statistics", "Replicazioni"
    elif choice == "2":
        return "infinite_horizon", "infinite-statistics", "Batch"
    else:
        print("Scelta non valida. Riprova.")
        return choose_horizon()

def plot_custom_graph_for_selected_seed(csv_paths, y_column, save_dir, sample_rate, selected_seed, x_label):
    plt.figure(figsize=FIGSIZE)

    if "mean_N_queue" in y_column:
        color_key = y_column.split('_')[3]  #estraggo il colore dalla colonna
        color = color_translation.get(color_key, color_key)
        title = f'Popolazione Media in coda per {color}'
        y_label = 'E[NQ]'
    elif "mean_queue" in y_column:
        parts = y_column.split('_')
        if len(parts) > 3:
            color_key = '_'.join(parts[2:-1])
        else:
            color_key = parts[2]
        color = color_translation.get(color_key, color_key)
        title = f'Tempo Medio di Attesa in Coda {color}'
        y_label = 'E[TQ]'
    else:
        title = y_column
        y_label = y_column

    #filtro il csv in base al seed che ho scelto
    selected_csv_path = csv_paths.get(selected_seed)
    if not selected_csv_path or not os.path.exists(selected_csv_path):
        raise FileNotFoundError(f"File CSV non trovato: {selected_csv_path}")

    data = pd.read_csv(selected_csv_path)

    if y_column not in data.columns:
        raise ValueError(f"Colonna '{y_column}' non trovata nel CSV per il seed {selected_seed}.")

    x_values = data['Simulation'][::sample_rate]
    y_values = data[y_column][::sample_rate]

    plt.plot(x_values, y_values, linestyle='-', linewidth='2', markersize=MARKERSIZE,
             color='b', marker='o', label=f'Seed: {seeds[selected_seed]}')
    plt.xlabel(x_label, fontsize=FONTSIZE_LABELS)
    plt.ylabel(y_label, fontsize=FONTSIZE_LABELS)
    plt.title(title, fontsize=FONTSIZE_TITLE, fontweight='bold', pad=20)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xticks(rotation=XTICK_ROTATION, fontsize=FONTSIZE_TICKS)
    plt.yticks(fontsize=FONTSIZE_TICKS)

    # Posizionamento della legenda fuori dal grafico
    plt.legend(fontsize=FONTSIZE_LEGEND, loc='upper left', bbox_to_anchor=(1, 1))

    # Aggiungi il bordo attorno al grafico
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.tight_layout(pad=2)

    # Crea la cartella di salvataggio se non esiste
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        print(f"Creata la cartella: {save_dir}\n")

    output_filename = f'{y_column}_line.png'
    output_file_path = os.path.join(save_dir, output_filename)

    # Salva il grafico
    try:
        plt.savefig(output_file_path, dpi=DPI, bbox_inches='tight')
        print(f"Grafico salvato in: {output_file_path}\n")
    except Exception as e:
        print(f"Errore durante il salvataggio del grafico: {e}")
    plt.close()


def plot_bar_graph(csv_paths, y_column, save_dir, selected_seed, sample_rate, x_label):
    # regolo la dimensione della figura per adattarla a più colonne
    plt.figure(figsize=(10, 6))

    if "mean_N_queue" in y_column:
        color_key = y_column.split('_')[3]  # Estrae il colore dalla colonna
        color = color_translation.get(color_key, color_key)
        title = f'Popolazione Media in Coda per {color}'
        y_label = 'E[NQ]'
    elif "mean_queue" in y_column:
        parts = y_column.split('_')
        if len(parts) > 3:
            color_key = '_'.join(parts[2:-1])
        else:
            color_key = parts[2]
        color = color_translation.get(color_key, color_key)
        title = f'Tempo Medio di Attesa in Coda {color}'
        y_label = 'E[TQ]'
    else:
        title = y_column
        y_label = y_column

    # Filtra solo il CSV relativo al seed specificato
    selected_csv_path = csv_paths.get(selected_seed)
    if not selected_csv_path or not os.path.exists(selected_csv_path):
        raise FileNotFoundError(f"File CSV non trovato: {selected_csv_path}")

    data = pd.read_csv(selected_csv_path)

    # Verifica se la colonna esiste nel CSV
    if y_column not in data.columns:
        raise ValueError(f"Colonna '{y_column}' non trovata nel CSV per il seed {selected_seed}.")

    # Campionamento dei valori della colonna
    y_values = data[y_column].values[::sample_rate]  # Campiona i valori della colonna
    x_values = range(0, len(y_values) * sample_rate, sample_rate)  # Creiamo l'asse X con gli indici campionati

    # Creazione del grafico a barre
    plt.bar(x_values, y_values, color='g', width=10, align='center', edgecolor='black')

    plt.xlabel(x_label, fontsize=FONTSIZE_LABELS)
    plt.ylabel(y_label, fontsize=FONTSIZE_LABELS)
    plt.title(title, fontsize=FONTSIZE_TITLE, fontweight='bold', pad=20)
    plt.xticks(x_values, x_values, fontsize=FONTSIZE_TICKS, rotation=45)
    plt.yticks(fontsize=FONTSIZE_TICKS)

    # Crea la cartella di salvataggio se non esiste
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        print(f"Creata la cartella: {save_dir}\n")

    output_filename = f'{y_column}_bar.png'
    output_file_path = os.path.join(save_dir, output_filename)

    # Salva il grafico
    try:
        plt.savefig(output_file_path, dpi=DPI, bbox_inches='tight')
        print(f"Grafico salvato in: {output_file_path}\n")
    except Exception as e:
        print(f"Errore durante il salvataggio del grafico: {e}")

    plt.close()

def plot_custom_graphs_across_seeds(csv_paths, y_column, save_dir, sample_rate,x_label):
    plt.figure(figsize=FIGSIZE)
    if "mean_N_queue" in y_column:
        color_key = y_column.split('_')[3]  # estraggo il colore dalla colonna
        color = color_translation.get(color_key, color_key)
        title = f'Popolazione Media in coda per {color}'
        y_label = 'E[NQ]'
    elif "mean_queue" in y_column:
        parts = y_column.split('_')
        if len(parts) > 3:
            color_key = '_'.join(parts[2:-1])
        else:
            color_key = parts[2]
        color = color_translation.get(color_key, color_key)
        title = f'Tempo Medio di Attesa in Coda {color}'
        y_label = 'E[TQ]'
    else:
        title = y_column
        y_label = y_column
    for i, (seed_key, csv_path) in enumerate(csv_paths.items()):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File CSV non trovato: {csv_path}")

        data = pd.read_csv(csv_path)

        # Verifica se la colonna esiste nel CSV
        if y_column not in data.columns:
            raise ValueError(f"Colonna '{y_column}' non trovata nel CSV per il seed {seed_key}.")

        x_values = data['Simulation'][::sample_rate]
        y_values = data[y_column][::sample_rate]

        # Plot solo con marker
        plt.plot(x_values, y_values, linestyle='-', markersize=MARKERSIZE,
                 color=COLORS[i], marker='o', label=f'Seed: {seeds[seed_key]}')

    plt.xlabel(x_label, fontsize=FONTSIZE_LABELS)
    plt.ylabel(y_label, fontsize=FONTSIZE_LABELS)
    plt.title(title, fontsize=FONTSIZE_TITLE, fontweight='bold', pad=20)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xticks(rotation=XTICK_ROTATION, fontsize=FONTSIZE_TICKS)
    plt.yticks(fontsize=FONTSIZE_TICKS)

    # Posizionamento della legenda fuori dal grafico
    plt.legend(fontsize=FONTSIZE_LEGEND, loc='upper left', bbox_to_anchor=(1,1))

    # Aggiunta di un bordo attorno al grafico
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.tight_layout(pad=2)

    # Salva i grafici nella cartella specificata
    output_filename = f'{y_column}_comparison.png'
    output_file_path = os.path.join(save_dir, output_filename)

    try:
        plt.savefig(output_file_path, dpi=DPI, bbox_inches='tight')
        print(f"Grafico salvato in: {output_file_path}\n")
    except Exception as e:
        print(f"Errore durante il salvataggio del grafico: {e}")
    plt.close()

def generate_comparison_graphs(sample_rate):
    graph_type = choose_graph_type()
    horizon_choice, file_prefix, x_label = choose_horizon()

    csv_paths = {seed_key: os.path.join(STATISTICS_OUTPUTS_DIR, f"{file_prefix}-{seed_key}.csv") for seed_key in seeds.keys()}
    sample_csv_path = next(iter(csv_paths.values()))  # Prende il percorso del primo CSV per ottenere le colonne

    if not os.path.exists(sample_csv_path):
        raise FileNotFoundError(f"File CSV non trovato: {sample_csv_path}")

    data = pd.read_csv(sample_csv_path)
    horizon_output_dir = os.path.join(GRAPHS_OUTPUTS_DIR, horizon_choice)

    for column in COLUMNS_TO_PLOT:
        if column in data.columns:
            print(f"Generazione del grafico comparativo per la colonna: {column}")
            if graph_type == "line":
                plot_custom_graph_for_selected_seed(csv_paths, y_column=column, save_dir=horizon_output_dir, sample_rate=sample_rate, selected_seed='1', x_label=x_label)
            elif graph_type == "bar":
                plot_bar_graph(csv_paths, y_column=column, save_dir=horizon_output_dir, selected_seed='1', sample_rate=sample_rate, x_label=x_label)
            elif graph_type== "multiple":
                plot_custom_graphs_across_seeds(csv_paths,y_column=column,save_dir=horizon_output_dir,sample_rate=sample_rate, x_label=x_label)
        else:
            print(f"Colonna {column} non trovata nei file CSV.")


generate_comparison_graphs(sample_rate=50)