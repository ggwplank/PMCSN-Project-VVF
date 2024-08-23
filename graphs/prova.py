import matplotlib.pyplot as plt
import pandas as pd
import os

from utils.constants import OUTPUTS_DIR

csv_file_path = '../simulation/outputs/temp_file.csv'

# Carica i dati dal file CSV
data = pd.read_csv(csv_file_path)

# Estrae le colonne necessarie per il grafico
simulation_runs = data['Simulation']
mean_service_hub_time = data['mean_service_red_time']

sample_rate = 16  # Mostra solo ogni 10 run
sampled_runs = simulation_runs[::sample_rate]
sampled_mean_service_hub_time = mean_service_hub_time[::sample_rate]

plt.figure(figsize=(16, 8))
plt.plot(sampled_runs, sampled_mean_service_hub_time, marker='o', linestyle='-', color='b')
plt.xlabel('Simulation Run')
plt.ylabel('Mean Service Time at Hub')
plt.title('Sampled Mean Service Time at Hub per Simulation Run')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, 'sampled_mean_service_time_at_hub.png'))
plt.show()

