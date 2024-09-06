import os
import pandas as pd
import matplotlib.pyplot as plt

from standard_simulator.utils.constants import seeds

# Definizioni Directory
ANALISI_STAZIONARIETA_DIR = os.path.join("../outputs", "statistics/analisi_della_stazionarietà")
ANALISI_TRANSITORIO_DIR = os.path.join("../outputs", "reports")

# Impostazioni grafiche
FIGSIZE = (18, 9)
DPI = 300
MARKERSIZE = 6
XTICK_ROTATION = 45
FONTSIZE_TITLE = 20
FONTSIZE_LABELS = 16
FONTSIZE_LEGEND = 14
FONTSIZE_TICKS = 12


## le colonne per il better simulator
COLUMNS_TO_SUM = [
    "mean_N_centre_hub", "mean_N_centre_red", "mean_N_centre_yellow_squadra","mean_N_centre_yellow_modulo",
     "mean_N_centre_green_modulo"
]

COLORS = ['b', 'g', 'r', 'c', 'm']  # Blu, Verde, Rosso, Ciano, Magenta


def plot_sum_of_columns_from_multiple_csvs(csv_folder, output_folder, sample_rate=15, final_sample_rate=1,
                                           switch_batch=0,
                                           y_min=None, y_max=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    csv_files = [f for f in os.listdir(csv_folder) if f.startswith('FA-infinite-statistics-') and f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"Nessun file CSV trovato nella cartella: {csv_folder}")
    plt.figure(figsize=FIGSIZE)
    plt.title('Evoluzione della Popolazione di Sistema', fontsize=FONTSIZE_TITLE, fontweight='bold', pad=20)
    for i, csv_file in enumerate(csv_files):
        seed = csv_file.split('-')[-1].replace('.csv', '')  # Estrai il numero di seed dal nome del file
        csv_path = os.path.join(csv_folder, csv_file)
        df = pd.read_csv(csv_path)
        missing_columns = [col for col in COLUMNS_TO_SUM if col not in df.columns]
        if missing_columns:
            print(f"Mancano le colonne {missing_columns} nel CSV per il seed {seed}.")
            continue
        # Somma delle colonne specifiche per ogni seed
        y_values = df[COLUMNS_TO_SUM].sum(axis=1)
        x_values = df['Simulation']

        # Campionamento iniziale (fino a switch_batch)
        x_values_initial = x_values[x_values < switch_batch][::sample_rate]  # Campionamento normale
        y_values_initial = y_values[x_values < switch_batch][::sample_rate]

        # Campionamento finale (dopo switch_batch)
        x_values_final = x_values[x_values >= switch_batch][::final_sample_rate]
        y_values_final = y_values[x_values >= switch_batch][::final_sample_rate]

        # Genera il grafico a linea per la parte iniziale
        plt.plot(x_values_initial, y_values_initial, linestyle='-', linewidth=2, markersize=MARKERSIZE,
                 color=COLORS[i % len(COLORS)], marker='o', label=f'Seed: {seeds[seed]}')

        # Genera il grafico a linea per la parte finale con maggiore dettaglio
        plt.plot(x_values_final, y_values_final, linestyle='-', linewidth=2, markersize=MARKERSIZE,
                 color=COLORS[i % len(COLORS)], marker='o')

    # Impostazioni Grafiche
    plt.xlabel('Batch', fontsize=FONTSIZE_LABELS)
    plt.ylabel('Popolazione di Sistema', fontsize=FONTSIZE_LABELS)
    plt.xticks(rotation=XTICK_ROTATION, fontsize=FONTSIZE_TICKS)
    plt.yticks(fontsize=FONTSIZE_TICKS)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Imposta il limite dell'asse Y
    if y_min is not None or y_max is not None:
        plt.ylim(y_min, y_max)
    plt.legend(fontsize=FONTSIZE_LEGEND, loc='upper left', bbox_to_anchor=(0, 1))

    # Aggiungi bordo attorno al grafico
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.tight_layout(pad=2)

    output_file_path = os.path.join(output_folder, 'Mean_N_centre_comparison.png')
    try:
        plt.savefig(output_file_path, dpi=DPI, bbox_inches='tight')
        print(f"Grafico salvato in: {output_file_path}")
    except Exception as e:
        print(f"Errore durante il salvataggio del grafico: {e}")

    plt.close()


def plot_columns_from_multiple_csvs(csv_folder, output_folder, sample_rate=10, final_sample_rate=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    csv_files = [f for f in os.listdir(csv_folder) if f.startswith('system-status-') if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"Nessun file CSV trovato nella cartella: {csv_folder}")
    dataframes = {}
    for csv_file in csv_files:
        seed = csv_file.split('-')[-1].replace('.csv', '')  # Estrai il numero di seed dal nome del file
        csv_path = os.path.join(csv_folder, csv_file)
        dataframes[seed] = pd.read_csv(csv_path)
    plt.figure(figsize=FIGSIZE)
    plt.title('Evoluzione della Popolazione di Sistema', fontsize=FONTSIZE_TITLE, fontweight='bold', pad=20)

    for i, (seed, df) in enumerate(dataframes.items()):
        if 'time' not in df.columns or 'system' not in df.columns:
            print(f"Colonne 'time' o 'system' non trovate nel CSV per il seed {seed}.")
            continue

        x_values_initial = df['time'][df['time'] < 9500][::sample_rate]
        y_values_initial = df['system'][df['time'] < 9500][::sample_rate]

        # Campionamento finale con un rate più piccolo
        x_values_final = df['time'][df['time'] >= 9500][::final_sample_rate]
        y_values_final = df['system'][df['time'] >= 9500][::final_sample_rate]

        plt.plot(x_values_initial, y_values_initial, linestyle='-', linewidth=2, markersize=MARKERSIZE,
                 color=COLORS[i % len(COLORS)], marker='o', label=f'Seed: {seeds[seed]}')

        plt.plot(x_values_final, y_values_final, linestyle='-', linewidth=2, markersize=MARKERSIZE,
                 color=COLORS[i % len(COLORS)], marker='o')

    # Impostazioni dell'asse e legenda
    plt.xlabel('Tempo', fontsize=FONTSIZE_LABELS)
    plt.ylabel('Popolazione di Sistema', fontsize=FONTSIZE_LABELS)
    plt.xticks(rotation=XTICK_ROTATION, fontsize=FONTSIZE_TICKS)
    plt.yticks(fontsize=FONTSIZE_TICKS)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend(fontsize=FONTSIZE_LEGEND, loc='upper right', bbox_to_anchor=(1, 1))

    # Aggiungi bordo attorno al grafico
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.tight_layout(pad=2)

    # Salva il grafico in output
    output_file_path = os.path.join(output_folder, 'system_comparison.png')
    try:
        plt.savefig(output_file_path, dpi=DPI, bbox_inches='tight')
        print(f"Grafico salvato in: {output_file_path}")
    except Exception as e:
        print(f"Errore durante il salvataggio del grafico: {e}")

    plt.close()


def run_analysis():
    choice = input("Vuoi fare i grafici per l'analisi del transitorio o della stazionarietà? (1/2): ").strip().lower()
    if choice == "1":
        plot_columns_from_multiple_csvs(ANALISI_TRANSITORIO_DIR, ANALISI_TRANSITORIO_DIR, sample_rate=8,
                                        final_sample_rate=1)
    elif choice == "2":
        plot_sum_of_columns_from_multiple_csvs(ANALISI_STAZIONARIETA_DIR, ANALISI_STAZIONARIETA_DIR, sample_rate=10,
                                               final_sample_rate=10, y_min=0, y_max=2)
    else:
        print("Scelta non valida. Inserisci 'transitorio' o 'stazionarietà'.")


run_analysis()

