import os
import pandas as pd
import matplotlib.pyplot as plt

# Impostazioni grafiche
FIGSIZE = (18, 9)
DPI = 300
MARKERSIZE = 6
XTICK_ROTATION = 45
FONTSIZE_TITLE = 20
FONTSIZE_LABELS = 16
FONTSIZE_LEGEND = 14
FONTSIZE_TICKS = 12

# Costanti per il plotting
COLUMNS_TO_PLOT = [
    "mean_queue_hub_time", "mean_queue_red_time", "mean_queue_yellow_time", "mean_queue_green_squadra_time",
    "mean_queue_green_modulo_time",
    "mean_N_queue_hub", "mean_N_queue_red", "mean_N_queue_yellow", "mean_N_queue_green_squadra",
    "mean_N_queue_green_modulo", "mean_response_hub_time", "mean_response_red_time", "mean_response_yellow_time",
    "mean_response_green_modulo_time","mean_response_green_squadra_time"
]

COLORS = ['b', 'g', 'r', 'c', 'm']  # Blu, Verde, Rosso, Ciano, Magenta


def plot_columns_from_multiple_csvs(csv_folder, output_folder, sample_rate=50):
    # Creazione della cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    # Cerca tutti i file CSV nella cartella specificata
    csv_files = [f for f in os.listdir(csv_folder) if f.startswith('FA-finite-statistics-') and f.endswith('.csv')]

    if not csv_files:
        raise FileNotFoundError(f"Nessun file CSV trovato nella cartella: {csv_folder}")

    # Legge tutti i CSV e li salva in un dizionario {seed: dataframe}
    dataframes = {}
    for csv_file in csv_files:
        seed = csv_file.split('-')[-1].replace('.csv', '')  # Estrai il numero di seed dal nome del file
        csv_path = os.path.join(csv_folder, csv_file)
        dataframes[seed] = pd.read_csv(csv_path)

    # Plot delle colonne specificate per tutti i CSV
    for column in COLUMNS_TO_PLOT:
        plt.figure(figsize=FIGSIZE)
        plt.title(f'Confronto per {column}', fontsize=FONTSIZE_TITLE, fontweight='bold', pad=20)

        for i, (seed, df) in enumerate(dataframes.items()):
            if column not in df.columns:
                print(f"Colonna '{column}' non trovata nel CSV per il seed {seed}.")
                continue

            # Estrai i valori campionati
            x_values = df['Simulation'][::sample_rate]  # Colonna 'Simulation' come asse x
            y_values = df[column][::sample_rate]  # Colonna corrente come asse y

            # Genera il grafico a linea
            plt.plot(x_values, y_values, linestyle='-', linewidth=2, markersize=MARKERSIZE,
                     color=COLORS[i % len(COLORS)], marker='o', label=f'Seed: {seed}')

        # Impostazioni dell'asse e legenda
        plt.xlabel('Settimane', fontsize=FONTSIZE_LABELS)
        plt.ylabel(column, fontsize=FONTSIZE_LABELS)
        plt.xticks(rotation=XTICK_ROTATION, fontsize=FONTSIZE_TICKS)
        plt.yticks(fontsize=FONTSIZE_TICKS)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(fontsize=FONTSIZE_LEGEND, loc='upper left', bbox_to_anchor=(1, 1))

        # Aggiungi bordo attorno al grafico
        plt.gca().spines['top'].set_visible(True)
        plt.gca().spines['right'].set_visible(True)
        plt.gca().spines['left'].set_linewidth(1.5)
        plt.gca().spines['bottom'].set_linewidth(1.5)
        plt.tight_layout(pad=2)

        # Salva il grafico in output
        output_file_path = os.path.join(output_folder, f'{column}_comparison.png')
        try:
            plt.savefig(output_file_path, dpi=DPI, bbox_inches='tight')
            print(f"Grafico salvato in: {output_file_path}")
        except Exception as e:
            print(f"Errore durante il salvataggio del grafico: {e}")

        plt.close()


# Esegui la funzione
csv_folder = r'C:\Users\luigi\PycharmProjects\PMCSN-Project-VVF\standard_simulator\outputs\statistics\analisi_del_transitorio'  # La cartella contenente i file CSV
output_folder = r'C:\Users\luigi\PycharmProjects\PMCSN-Project-VVF\standard_simulator\outputs\statistics\analisi_del_transitorio'  # La cartella dove salvare i grafici

plot_columns_from_multiple_csvs(csv_folder, output_folder, sample_rate=15)
